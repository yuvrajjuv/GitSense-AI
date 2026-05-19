def generate_ai_summary(profile, repos):

    repo_count = profile["public_repos"]
    followers = profile["followers"]

    languages = []

    for repo in repos:

        language = repo["language"]

        if language and language not in languages:
            languages.append(language)

    top_languages = ", ".join(languages[:3])

    # AI Summary Logic

    if repo_count > 20:

        return f"""
🚀 This developer is highly active on GitHub.

Primary technologies include: {top_languages}.

The profile demonstrates:
✅ Strong project-building consistency
✅ Active development mindset
✅ Good potential in AI/Open Source ecosystem

Recommended Role:
👨‍💻 AI/ML Engineer or Full Stack Developer
        """

    elif repo_count > 10:

        return f"""
👨‍💻 This developer is consistently building projects.

Primary technologies include: {top_languages}.

The profile indicates:
✅ Growing technical skills
✅ Strong learning capability
✅ Good development activity
        """

    else:

        return f"""
🌱 Beginner developer detected.

Primary technologies include: {top_languages}.

Recommendations:
✅ Build more public projects
✅ Improve GitHub activity
✅ Add documentation and README files
        """