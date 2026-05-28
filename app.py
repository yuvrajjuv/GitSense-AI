import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from fpdf import FPDF

from utils.github_api import (
    get_github_profile,
    get_user_repos
)

from utils.ai_analyzer import generate_ai_summary

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="GitSense AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}

.stMetric {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 12px;
}

[data-testid="stMetric"] {
    background-color: #1c1f26;
    border: 1px solid #31333F;
    padding: 20px;
    border-radius: 15px;
}

.repo-card {
    background-color: #161B22;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    border: 1px solid #30363D;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.title("🚀 GitSense AI")
st.subheader("AI-Powered GitHub Productivity Analyzer")

st.markdown("---")

# ---------------- INPUT ---------------- #

username = st.text_input(
    "Enter GitHub Username"
)

# ---------------- MAIN APP ---------------- #

if username:

    profile = get_github_profile(username)

    if profile:

        repos = get_user_repos(username)

        st.success(
            f"GitHub Profile Found: {username}"
        )

        # ---------------- PROFILE SECTION ---------------- #

        col1, col2 = st.columns([1, 3])

        with col1:

            st.image(
                profile["avatar_url"],
                width=180
            )

        with col2:

            st.markdown(
                f"# {profile['name']}"
            )

            if profile["bio"]:
                st.write(profile["bio"])

            st.write(
                f"📍 Location: {profile['location']}"
            )

            st.write(
                f"👥 Followers: {profile['followers']}"
            )

            st.write(
                f"📦 Public Repositories: {profile['public_repos']}"
            )

            st.write(
                f"🔗 GitHub: {profile['html_url']}"
            )

        # ---------------- REPOSITORY ANALYSIS ---------------- #

        st.markdown("---")
        st.markdown("## 📊 Repository Analysis")

        left_col, right_col = st.columns(2)

        language_count = {}

        total_stars = 0

        with left_col:

            st.markdown("### ⭐ Top Repositories")

            for repo in repos[:5]:

                total_stars += repo["stargazers_count"]

                st.markdown(f"""
<div class="repo-card">

### 🔥 {repo['name']}

⭐ Stars: {repo['stargazers_count']}  
🍴 Forks: {repo['forks_count']}  
🧠 Language: {repo['language']}

</div>
""", unsafe_allow_html=True)

                language = repo["language"]

                if language:

                    if language in language_count:
                        language_count[language] += 1
                    else:
                        language_count[language] = 1

        with right_col:

            st.markdown("### 💻 Most Used Languages")

            if language_count:

                df = pd.DataFrame({
                    "Language": list(language_count.keys()),
                    "Count": list(language_count.values())
                })

                fig = px.pie(
                    df,
                    names="Language",
                    values="Count",
                    hole=0.5
                )

                fig.update_layout(height=500)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        # ---------------- STARS GRAPH ---------------- #

        st.markdown("---")
        st.markdown("## 📈 Repository Stars Analytics")

        repo_names = [repo["name"] for repo in repos[:5]]
        repo_stars = [repo["stargazers_count"] for repo in repos[:5]]

        stars_df = pd.DataFrame({
            "Repository": repo_names,
            "Stars": repo_stars
        })

        fig_bar = px.bar(
            stars_df,
            x="Repository",
            y="Stars",
            text="Stars"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        # ---------------- AI SCORE ---------------- #

        st.markdown("---")
        st.markdown("## 🤖 AI Developer Score")

        score = (
            profile["followers"] * 2
            + profile["public_repos"] * 3
            + total_stars
        )

        final_score = min(score, 100)

        st.progress(final_score / 100)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Developer Score",
                f"{final_score}/100"
            )

        with col2:
            st.metric(
                "Followers",
                profile["followers"]
            )

        with col3:
            st.metric(
                "Repositories",
                profile["public_repos"]
            )

        with col4:
            st.metric(
                "Total Stars",
                total_stars
            )

        # ---------------- PERFORMANCE MESSAGE ---------------- #

        if final_score > 80:

            st.success("""
🚀 Excellent Open Source Developer

Strong GitHub presence with high community impact.
            """)

        elif final_score > 40:

            st.info("""
👨‍💻 Good Developer

Consistent development activity detected.
            """)

        else:

            st.warning("""
🌱 Beginner Developer

Keep building and contributing more projects.
            """)

        # ---------------- SKILL DETECTOR ---------------- #

        st.markdown("---")
        st.markdown("## 🧠 Skill Detection")

        detected_skills = []

        skills_map = {
            "Python": "AI/ML",
            "JavaScript": "Frontend Development",
            "TypeScript": "Frontend Development",
            "HTML": "Web Design",
            "CSS": "UI/UX",
            "Docker": "DevOps",
            "Shell": "DevOps",
            "C++": "System Programming",
            "Java": "Backend Development"
        }

        for lang in language_count.keys():

            if lang in skills_map:
                detected_skills.append(skills_map[lang])

        detected_skills = list(set(detected_skills))

        if detected_skills:

            for skill in detected_skills:
                st.success(f"✅ {skill}")

        else:
            st.info("No major skills detected.")

        # ---------------- AI INSIGHTS ---------------- #

        st.markdown("---")
        st.markdown("## 🧠 AI Insights")

        ai_summary = generate_ai_summary(
            profile,
            repos
        )

        st.info(ai_summary)

        # ---------------- RECRUITER MODE ---------------- #

        st.markdown("---")
        st.markdown("## 🧑‍💼 Recruiter AI Recommendation")

        if final_score >= 80:

            st.success("""
✅ Highly Recommended for Hiring

This developer demonstrates strong GitHub consistency,
good open-source engagement,
and strong technical capabilities.
            """)

        elif final_score >= 50:

            st.info("""
⚡ Recommended

This developer shows good development activity
and learning capability.
            """)

        else:

            st.warning("""
📚 Beginner Level Candidate

Potential detected but needs more practical exposure.
            """)

        # ---------------- PDF REPORT ---------------- #

        st.markdown("---")
        st.markdown("## 📄 Download Developer Report")

        pdf = FPDF()

        pdf.add_page()

        pdf.set_font("Arial", size=16)

        pdf.cell(200, 10, txt="GitSense AI Report", ln=True)

        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Developer: {profile['name']}", ln=True)
        pdf.cell(200, 10, txt=f"Followers: {profile['followers']}", ln=True)
        pdf.cell(200, 10, txt=f"Repositories: {profile['public_repos']}", ln=True)
        pdf.cell(200, 10, txt=f"Developer Score: {final_score}", ln=True)

        pdf.output("developer_report.pdf")

        with open("developer_report.pdf", "rb") as file:

            st.download_button(
                label="📥 Download PDF Report",
                data=file,
                file_name="developer_report.pdf",
                mime="application/pdf"
            )

    else:

        st.error(
            "GitHub user not found"
        )