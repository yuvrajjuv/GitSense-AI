import streamlit as st
import pandas as pd
import plotly.express as px

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

        # ---------------- REPOSITORIES ---------------- #

        repos = get_user_repos(username)

        st.markdown("---")

        st.markdown(
            "## 📊 Repository Analysis"
        )

        left_col, right_col = st.columns(2)

        language_count = {}

        # ---------------- LEFT SIDE ---------------- #

        with left_col:

            st.markdown(
                "### ⭐ Top Repositories"
            )

            for repo in repos[:5]:

                st.markdown(
                    f"""
### 🔥 {repo['name']}

⭐ Stars: {repo['stargazers_count']}  
🍴 Forks: {repo['forks_count']}  
🧠 Language: {repo['language']}
                    """
                )

                language = repo["language"]

                if language:

                    if language in language_count:
                        language_count[language] += 1

                    else:
                        language_count[language] = 1

        # ---------------- RIGHT SIDE ---------------- #

        with right_col:

            st.markdown(
                "### 💻 Most Used Languages"
            )

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

                fig.update_layout(
                    height=500
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        # ---------------- AI SCORE ---------------- #

        st.markdown("---")

        st.markdown(
            "## 🤖 AI Developer Score"
        )

        score = (
            profile["followers"] * 2
            + profile["public_repos"] * 3
        )

        final_score = min(score, 100)

        st.progress(
            final_score / 100
        )

        col1, col2, col3 = st.columns(3)

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

        # ---------------- AI INSIGHTS ---------------- #

        st.markdown("---")

        st.markdown(
            "## 🧠 AI Insights"
        )

        ai_summary = generate_ai_summary(
            profile,
            repos
        )

        st.info(ai_summary)

    else:

        st.error(
            "GitHub user not found"
        )