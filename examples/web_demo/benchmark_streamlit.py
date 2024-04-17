import streamlit as st
import numpy as np
from scalesafe.benchmarking import Benchmarker

def run_benchmark(api_key, benchmark):
    dataset = Benchmarker(benchmark, api_key=api_key)  # Example bias screening for employment AI in New York
    
    for item in dataset:
        # Your AI model here
        output = True if np.random.random() > 0.5 else False
        dataset.answer(output, item['id'])  # We add our responses to the buffer

    dataset.post_answers()  # We send them to our audit team for analysis
    st.success("Benchmark completed and results posted!")

# Streamlit user interface
st.title("ScaleSafe Benchmarking")

# Explainer text
st.markdown("""
Benchmarking is an important process in AI safety. By running benchmarks, you can evaluate the effectiveness of your AI models, algorithms, or systems, and compare them to industry standards or previous versions.

In this Streamlit application, you can run a benchmark by providing your ScaleSafe API Key and the benchmark name. The benchmarking process will simulate the evaluation of an AI model.
""")

api_key = st.text_input("Enter your SCALESAFE_API_KEY:")
benchmark = st.text_input("Enter the benchmark name:")

benchmark_options = ["simpleMath", "nyEmploymentScreeningText"]
selected_benchmark = st.selectbox("Or select a benchmark below:", benchmark_options)

if selected_benchmark:
    benchmark = selected_benchmark

if st.button("Run Benchmark"):
    if api_key and benchmark:
        run_benchmark(api_key, benchmark)
    else:
        st.error("Please provide both the API Key and the benchmark name.")

