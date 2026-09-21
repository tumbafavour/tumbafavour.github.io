# tumbafavour.github.io

My personal portfolio — live at **https://tumbafavour.github.io**

## How it works

The site is a single `index.html` hosted on GitHub Pages. On every visit it fetches my public repositories from the GitHub API, so **new projects appear automatically** — no site edits needed.

- **Selected work** at the top of the Projects section is hand-written in `PROFILE.featured`, so my flagship projects always lead — each entry's `repo` must match the GitHub repo name.
- Everything else appears under **More from GitHub**, pulled live from the API.
- Repos tagged with the **`portfolio`** topic are featured there; if none are tagged, it shows all my non-fork repos instead.
- Forks, this site's own repo, and anything already in `PROFILE.featured` are hidden from that grid.

## Résumé

`Favour_Tumba_Resume.pdf` at the repo root is linked from the hero and the contact section. It's generated, not hand-edited:

```bash
python resume/build_resume.py
```

Edit the content blocks in `resume/build_resume.py` and re-run it. The script embeds fonts, adds real hyperlinks, and auto-fits the layout to a single page.

## Showcasing a project

1. Push the project to GitHub with a good description.
2. On the repo page, click the ⚙️ next to **About** and add the topic `portfolio`.
3. Done — it appears on the site.
