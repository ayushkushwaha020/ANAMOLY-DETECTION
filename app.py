import io
import math
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="ALGOMIND | Component Anomaly Detection", page_icon="⚡", layout="wide")

st.title("ALGOMIND — Component Anomaly Detection")
st.caption("AI-assisted burn-in & screening analysis • SIH PS 26170 • Prototype MVP")

@st.cache_data
def demo_data(n=80, points=20, seed=42):
    rng=np.random.default_rng(seed)
    rows=[]
    for c in range(n):
        cid=f"C{c+1:04d}"
        abnormal=c in [11,27,53,68]
        bt=rng.normal(48,2); bc=rng.normal(.80,.05); bv=rng.normal(5,.03)
        for t in range(points):
            temp=bt+.18*t+rng.normal(0,.35)
            cur=bc+.002*t+rng.normal(0,.008)
            vol=bv+rng.normal(0,.008)
            if abnormal and t>10:
                temp+=(t-10)*.55
                cur+=(t-10)*.010
                vol+=rng.normal(0,.035)
            rows.append([cid,t,temp,cur,vol])
    return pd.DataFrame(rows,columns=["component_id","time_min","temperature_c","current_a","voltage_v"])

def robust_z(series):
    s=pd.to_numeric(series, errors="coerce").fillna(0).to_numpy(dtype=float)
    med=np.median(s)
    mad=np.median(np.abs(s-med))
    if mad < 1e-12:
        sd=np.std(s)
        return np.abs((s-med)/(sd+1e-9))
    return np.abs((s-med)/(1.4826*mad+1e-9))

def score_anomalies(df):
    # Lightweight, explainable prototype:
    # robust deviation + time-derivative deviation across multiple parameters.
    x=df.copy()
    g=x.groupby("component_id")
    x["temp_rate"]=g["temperature_c"].transform(lambda s:s.diff().fillna(0))
    x["current_rate"]=g["current_a"].transform(lambda s:s.diff().fillna(0))
    x["voltage_rate"]=g["voltage_v"].transform(lambda s:s.diff().fillna(0))

    component_features=x.groupby("component_id").agg(
        temp_mean=("temperature_c","mean"),
        temp_max=("temperature_c","max"),
        temp_change=("temperature_c",lambda s:float(s.iloc[-1]-s.iloc[0])),
        current_mean=("current_a","mean"),
        current_change=("current_a",lambda s:float(s.iloc[-1]-s.iloc[0])),
        voltage_std=("voltage_v","std"),
        temp_rate_max=("temp_rate","max"),
        current_rate_max=("current_rate","max"),
        voltage_rate_max=("voltage_rate","max")
    ).fillna(0).reset_index()

    cols=["temp_change","current_change","voltage_std","temp_rate_max","current_rate_max","voltage_rate_max"]
    scores=np.zeros(len(component_features))
    for c in cols:
        scores += robust_z(component_features[c])
    scores /= len(cols)
    component_features["anomaly_score"]=scores
    threshold=float(np.quantile(scores, 0.90))
    component_features["status"]=np.where(scores>=threshold,"Potential anomaly","Normal")
    return x, component_features.sort_values("anomaly_score",ascending=False), threshold

with st.sidebar:
    st.header("Data")
    upload=st.file_uploader("Upload burn-in CSV",type=["csv"])
    st.caption("Required: component_id, time_min, temperature_c, current_a, voltage_v")
    st.divider()
    st.write("Prototype method")
    st.caption("Robust multi-parameter + time-trend anomaly scoring. No SciPy or scikit-learn required.")

df=pd.read_csv(upload) if upload else demo_data()
required=["component_id","time_min","temperature_c","current_a","voltage_v"]
missing=[c for c in required if c not in df.columns]
if missing:
    st.error("Missing columns: "+", ".join(missing))
    st.stop()

df=df[required].copy()
for c in required[1:]:
    df[c]=pd.to_numeric(df[c],errors="coerce")
df=df.dropna().sort_values(["component_id","time_min"]).reset_index(drop=True)

analyzed, summary, threshold=score_anomalies(df)

a,b,c,d=st.columns(4)
a.metric("Components analyzed",len(summary))
b.metric("Potential anomalies",int((summary.status=="Potential anomaly").sum()))
c.metric("Normal",int((summary.status=="Normal").sum()))
d.metric("Readings analyzed",len(analyzed))

tab1,tab2,tab3,tab4,tab5=st.tabs(["Overview","Flagged components","Component analysis","Trends","Export"])

with tab1:
    st.subheader("Screening overview")
    st.dataframe(summary.head(15),use_container_width=True,hide_index=True)
    st.info("An anomaly indicates behavior that differs from the learned/robust baseline in this prototype. It is not a declaration that a component is defective; engineer review is required.")

with tab2:
    st.subheader("Potentially anomalous components")
    st.caption("Flagged for engineer review — these components are not confirmed defective.")
    flagged=summary.loc[summary["status"]=="Potential anomaly", [
        "component_id","anomaly_score","temp_change","current_change",
        "voltage_std","temp_rate_max","current_rate_max","voltage_rate_max"
    ]].copy()
    flagged=flagged.rename(columns={
        "component_id":"Component ID",
        "anomaly_score":"Anomaly score",
        "temp_change":"Temperature change (°C)",
        "current_change":"Current change (A)",
        "voltage_std":"Voltage variation (V)",
        "temp_rate_max":"Max temperature rise/step",
        "current_rate_max":"Max current rise/step",
        "voltage_rate_max":"Max voltage change/step"
    })
    st.metric("Components flagged for review", len(flagged))
    st.dataframe(flagged, use_container_width=True, hide_index=True)
    st.download_button("Download flagged components", flagged.to_csv(index=False).encode(),
                       "ALGOMIND_flagged_components.csv", "text/csv")

with tab3:
    selected=st.selectbox("Select component",summary.component_id.tolist())
    s=analyzed[analyzed.component_id==selected]
    rec=summary[summary.component_id==selected].iloc[0]
    x,y,z=st.columns(3)
    x.metric("Status",rec.status)
    y.metric("Anomaly score",f"{rec.anomaly_score:.2f}")
    z.metric("Screening threshold",f"{threshold:.2f}")
    st.line_chart(s.set_index("time_min")[["temperature_c","current_a","voltage_v"]])

    st.write("**Why it was flagged (prototype indicators):**")
    reasons=[]
    if s.temperature_c.iloc[-1]-s.temperature_c.iloc[0] > 8:
        reasons.append("Temperature shows a strong rise across the test.")
    if s.current_a.iloc[-1]-s.current_a.iloc[0] > .12:
        reasons.append("Current shows noticeable drift.")
    if s.voltage_v.std() > .02:
        reasons.append("Voltage varies more than the typical stable pattern.")
    if not reasons:
        reasons.append("The combined multi-parameter/time-trend pattern differs from the baseline.")
    for r in reasons:
        st.write("• "+r)

with tab4:
    metric=st.selectbox("Parameter",["temperature_c","current_a","voltage_v"])
    comp=st.selectbox("Component",summary.component_id.tolist(),key="trend")
    st.line_chart(analyzed[analyzed.component_id==comp].set_index("time_min")[[metric]])

with tab5:
    st.download_button("Download screening report",summary.to_csv(index=False).encode(),"ALGOMIND_screening_report.csv","text/csv")
    st.download_button("Download analyzed readings",analyzed.to_csv(index=False).encode(),"ALGOMIND_analyzed_readings.csv","text/csv")

st.divider()
st.caption("ALGOMIND prototype • Final screening decisions remain with the engineer.")
