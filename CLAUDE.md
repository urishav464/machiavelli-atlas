@AGENTS.md

## הערות ל-Claude

- **סקילים (אם שמורים בחשבון):** `atlas-fact-sheet` (תיק עובדות), `atlas-fact-check` (בדיקה עצמאית), `atlas-chapter-build` (בנייה, בדיקה ופרסום). מפעילים אותם לפי השלב.
- **סוכנים:** `.claude/agents/atlas-researcher.md` ו-`.claude/agents/atlas-fact-checker.md`. אם הם לא נטענו, מעבירים לסוכן general-purpose את גוף הקובץ כהנחיה.
- **הפרויקט ב-claude.ai:** קוראים סיכומי פרקים עם `Projects` → `project_read`. שומרים תיקי עובדות עם `project_write`, בתור `claude/אטלס-תיק-עובדות-...`.
- **הארטיפקט:** כלי `Artifact`, `action:"publish"`, `url` של האטלס, `file_path` של `index.html`, ו-`files` עם כל הקבצים החדשים.
- **הרשאת דחיפה ל-GitHub:** `add_repo urishav464/machiavelli-atlas` עם `access:"push"`.
- **ניסוח ל-commit** (חובה):
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: <קישור השיחה הנוכחית>
  ```
