import os
import streamlit as st
import pandas as pd
import plotly.express as px

from pdf_reader import extract_pdf_text
from ollama_service import ask_ollama
from analytics import get_document_stats, get_top_keywords, get_complexity_score
from grammar_checker import generate_error_report   
os.makedirs("uploads", exist_ok=True)

st.set_page_config(
    page_title="AI PDF Intelligence Dashboard",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #0b0f19;
    color: #f8fafc;
}

.hero {
    padding: 40px;
    border-radius: 26px;
    background: linear-gradient(135deg, #1e3a8a, #2563eb, #7c3aed);
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 20px 50px rgba(37,99,235,0.35);
}

.hero h1 {
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 12px;
}

.hero p {
    font-size: 18px;
    color: #e0e7ff;
}

.feature-row {
    display: flex;
    gap: 12px;
    margin-top: 22px;
    flex-wrap: wrap;
}

.feature-pill {
    background: rgba(255,255,255,0.15);
    padding: 10px 16px;
    border-radius: 999px;
    font-weight: 600;
}

.metric-card {
    background: linear-gradient(180deg, #ffffff, #f8fafc);
    color: #0f172a;
    border-radius: 22px;
    padding: 25px;
    min-height: 160px;
    box-shadow: 0 14px 35px rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.12);
}

.metric-card h2 {
    color: #2563eb;
    font-size: 36px;
    margin-bottom: 4px;
}

.metric-card h4 {
    color: #111827;
    margin-bottom: 8px;
}

.metric-card p {
    color: #475569;
    font-size: 14px;
}

.section-card {
    background: #111827;
    border: 1px solid #1f2937;
    padding: 26px;
    border-radius: 22px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    margin-bottom: 24px;
}

.info-box {
    background: #0f172a;
    border-left: 5px solid #3b82f6;
    padding: 16px;
    border-radius: 14px;
    margin-top: 12px;
    color: #dbeafe;
}

.small-muted {
    color: #94a3b8;
    font-size: 14px;
}

.upload-box {
    background: #111827;
    border: 1px dashed #475569;
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>📄 AI PDF Intelligence Dashboard</h1>
    <p>Upload any PDF and convert it into a complete AI-powered report with summary, insights, charts, keywords, complexity analysis, and PDF question answering.</p>
    <div class="feature-row">
        <div class="feature-pill">🧠 AI Summary</div>
        <div class="feature-pill">📊 Visual Analytics</div>
        <div class="feature-pill">🔑 Keyword Mining</div>
        <div class="feature-pill">💬 Chat With PDF</div>
        <div class="feature-pill">📈 Report Dashboard</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    pdf_path = os.path.join("uploads", uploaded_file.name)

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Reading and analyzing PDF..."):
        text, pages = extract_pdf_text(pdf_path)

    if not text.strip():
        st.error("No readable text found in this PDF.")
        st.stop()

    stats = get_document_stats(text, pages)
    keywords = get_top_keywords(text)
    complexity = get_complexity_score(text)

    st.success("PDF uploaded and analyzed successfully!")

    st.markdown("## 📌 Document Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{stats['pages']}</h2>
            <h4>Pages</h4>
            <p>Total number of pages detected in the uploaded PDF document.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{stats['words']}</h2>
            <h4>Words</h4>
            <p>Total words extracted from the PDF. This helps measure document length.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{stats['sentences']}</h2>
            <h4>Sentences</h4>
            <p>Total sentence count used for readability and complexity analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{stats['read_time']} min</h2>
            <h4>Reading Time</h4>
            <p>Estimated time required to read this PDF at normal reading speed.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <b>What these cards mean:</b><br>
        Pages show document size, words show content volume, sentences help understand structure, and reading time estimates how long a person may need to read the PDF.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🧠 Executive AI Summary")

        if st.button("Generate Full AI Report"):
            prompt = f"""
            Create a professional PDF report summary.

            Format:
            Title:
            Main Objective:
            Key Points:
            Important Findings:
            Problems Discussed:
            Final Conclusion:
            Recommendations:

            PDF Content:
            {text[:9000]}
            """

            with st.spinner("Generating professional report using Ollama Mistral..."):
                summary = ask_ollama(prompt)

            st.markdown(summary)

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📊 Complexity Report")

        st.metric("Reading Level", complexity["level"])
        st.metric("Avg Sentence Length", f"{complexity['avg_sentence_length']} words")
        st.metric("Avg Word Length", f"{complexity['avg_word_length']} chars")

        st.markdown("""
        <div class="info-box">
        This section explains how easy or difficult the PDF is to read based on sentence length and word size.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("## 🔑 Keyword Intelligence")

    if keywords:
        keyword_df = pd.DataFrame(keywords, columns=["Keyword", "Count"])

        k1, k2 = st.columns([1, 1.4])

        with k1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Top Keywords")
            st.dataframe(keyword_df, use_container_width=True)

            st.markdown("""
            <div class="info-box">
            These keywords show the most repeated and important terms in the PDF.
            They help identify the main topic of the document.
            </div>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with k2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            fig = px.bar(
                keyword_df.sort_values("Count"),
                x="Count",
                y="Keyword",
                orientation="h",
                title="Top Keyword Frequency"
            )

            fig.update_layout(
                template="plotly_dark",
                height=420,
                paper_bgcolor="#111827",
                plot_bgcolor="#111827"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("## 📈 Document Analytics")

    a1, a2 = st.columns(2)

    chart_data = pd.DataFrame({
        "Metric": ["Pages", "Words", "Sentences", "Reading Time"],
        "Value": [
            stats["pages"],
            stats["words"],
            stats["sentences"],
            stats["read_time"]
        ]
    })

    with a1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        fig2 = px.pie(
            chart_data,
            names="Metric",
            values="Value",
            title="Document Metric Distribution",
            hole=0.45
        )

        fig2.update_layout(
            template="plotly_dark",
            height=420,
            paper_bgcolor="#111827",
            plot_bgcolor="#111827"
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with a2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        fig3 = px.bar(
            chart_data,
            x="Metric",
            y="Value",
            title="Document Statistics Comparison",
            text="Value"
        )

        fig3.update_layout(
            template="plotly_dark",
            height=420,
            paper_bgcolor="#111827",
            plot_bgcolor="#111827"
        )

        st.plotly_chart(fig3, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <b>Chart explanation:</b><br>
        The pie chart shows how different document metrics compare as a whole.
        The bar chart gives a clear comparison of pages, words, sentences, and reading time.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("## 🤖 AI Insights and Recommendations")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    if st.button("Generate AI Insights"):
        prompt = f"""
        Analyze this PDF and provide:

        1. Main theme
        2. Important topics
        3. Strengths of the document
        4. Weak areas
        5. Practical recommendations
        6. Best use case of this document

        PDF Content:
        {text[:9000]}
        """

        with st.spinner("Generating AI insights..."):
            insights = ask_ollama(prompt)

        st.markdown(insights)

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("## 📄 Extracted PDF Text Preview")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    with st.expander("Show extracted PDF text"):
        st.text_area("PDF Text", text[:7000], height=350)

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("## 💬 Chat With PDF")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    user_question = st.text_input("Ask any question from this PDF")

    if st.button("Ask PDF"):
        if user_question.strip() == "":
            st.warning("Please enter a question.")
        else:
            prompt = f"""
            You are a PDF question-answering assistant.
            Answer only using the PDF content.

            PDF Content:
            {text[:10000]}

            User Question:
            {user_question}

            Give a clear and helpful answer.
            """

            with st.spinner("Finding answer from PDF..."):
                answer = ask_ollama(prompt)

            st.markdown("### AI Answer")
            st.write(answer)

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("## 📝 Grammar, Spelling and Sentence Error Report")

    try:
        if text is None or str(text).strip() == "":
            st.warning("PDF text is empty. Grammar report cannot be generated.")
        else:
            with st.spinner("Checking grammar and spelling..."):
                error_report = generate_error_report(text)

            if not isinstance(error_report, dict):
                st.warning("Grammar checker returned invalid report.")
            else:
                st.success("Grammar report generated successfully!")

                total_errors = error_report.get("total_errors", 0)
                spelling_count = error_report.get("spelling_count", 0)
                sentence_count = error_report.get("sentence_count", 0)

                e1, e2, e3 = st.columns(3)

                with e1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2>{total_errors}</h2>
                        <h4>Total Errors</h4>
                        <p>Total spelling, sentence, punctuation, and formatting issues found in the PDF.</p>
                    </div>
                    """, unsafe_allow_html=True)

                with e2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2>{spelling_count}</h2>
                        <h4>Spelling Mistakes</h4>
                        <p>Incorrect or unknown words detected from the extracted PDF text.</p>
                    </div>
                    """, unsafe_allow_html=True)

                with e3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2>{sentence_count}</h2>
                        <h4>Sentence Issues</h4>
                        <p>Capitalization, punctuation, spacing, and incomplete sentence issues.</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("""
                <div class="info-box">
                <b>What this report means:</b><br>
                This section checks the PDF text line by line and finds spelling mistakes, punctuation issues,
                capitalization errors, short sentences, and spacing problems.
                </div>
                """, unsafe_allow_html=True)

                error_chart_data = pd.DataFrame({
                    "Error Type": ["Spelling Mistakes", "Sentence Issues"],
                    "Count": [spelling_count, sentence_count]
                })

                g1, g2 = st.columns(2)

                with g1:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)

                    fig_error_bar = px.bar(
                        error_chart_data,
                        x="Error Type",
                        y="Count",
                        text="Count",
                        title="Error Type Comparison"
                    )

                    fig_error_bar.update_layout(
                        template="plotly_dark",
                        height=420,
                        paper_bgcolor="#111827",
                        plot_bgcolor="#111827"
                    )

                    st.plotly_chart(fig_error_bar, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with g2:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)

                    fig_error_pie = px.pie(
                        error_chart_data,
                        names="Error Type",
                        values="Count",
                        title="Error Distribution",
                        hole=0.45
                    )

                    fig_error_pie.update_layout(
                        template="plotly_dark",
                        height=420,
                        paper_bgcolor="#111827",
                        plot_bgcolor="#111827"
                    )

                    st.plotly_chart(fig_error_pie, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("### 🔴 Spelling Mistakes With Line Number")

                spelling_errors = error_report.get("spelling_errors", [])

                if spelling_errors:
                    spelling_df = pd.DataFrame(spelling_errors)
                    st.dataframe(spelling_df, use_container_width=True)
                else:
                    st.success("No major spelling mistakes found.")

                st.markdown("### 🟠 Sentence and Grammar Issues With Line Number")

                sentence_errors = error_report.get("sentence_errors", [])

                if sentence_errors:
                    sentence_df = pd.DataFrame(sentence_errors)
                    st.dataframe(sentence_df, use_container_width=True)
                else:
                    st.success("No major sentence issues found.")

                st.markdown("### 🤖 AI Grammar Improvement Report")

                if st.button("Generate AI Grammar Improvement Suggestions"):
                    sample_text_for_grammar = text[:6000]

                    prompt = f"""
                    Analyze the following PDF text for grammar, sentence structure, clarity, spelling,
                    punctuation, and academic writing quality.

                    Give output in this format:

                    1. Overall Writing Quality
                    2. Common Grammar Problems
                    3. Spelling and Word Choice Problems
                    4. Sentence Structure Problems
                    5. Professional Improvement Suggestions
                    6. Corrected Sample Paragraph

                    PDF Text:
                    {sample_text_for_grammar}
                    """

                    with st.spinner("Generating grammar improvement report using Ollama..."):
                        grammar_ai_report = ask_ollama(prompt)

                    st.markdown(grammar_ai_report)

    except Exception as e:
        st.error("Grammar report failed.")
        st.exception(e)

else:
    st.info("Upload a PDF file to start the dashboard.")
    st.stop()