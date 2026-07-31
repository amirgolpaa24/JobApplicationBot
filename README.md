# JobApplicationBot

This repository stores LaTeX resumes and cover letters for an automated job-application workflow. It keeps reusable master files in one place, stores each job application separately, and uses GitHub Actions to compile PDFs.

## Structure

Reusable source files live in `master/`:

- `master/Amir_Mirzai_Golpayegani_master_resume.tex`
- `master/Amir_Mirzai_Golpayegani_cover_letter_example.tex`

Each application should use its own folder:

```text
applications/
└── Job_<job_number>/
    ├── resume.tex
    ├── resume.pdf
    ├── cover_letter.tex
    ├── cover_letter.pdf
    └── metadata.json
```

Keep `metadata.json` with the LaTeX files so each generated application can be traced back to the job posting.

Recommended metadata:

```json
{
  "job_number": "",
  "position_title": "",
  "company": "",
  "location": "",
  "work_arrangement": "",
  "job_type": "",
  "job_id": "",
  "source_url": "",
  "prepared_date": ""
}
```

## PDF Compilation

The workflow in `.github/workflows/compile-latex.yml` runs on pushes to `main` that change application `.tex` files, and it can also be started manually from the GitHub Actions tab.

For every `applications/Job_*` folder, it compiles `resume.tex` and `cover_letter.tex` with `latexmk -pdf` when those files exist. Generated or updated PDFs are committed back to the same branch. PDF-only commits do not restart the workflow.

If a compilation fails, open the failed run in the Actions tab and inspect the log for the relevant job folder.

## Notes

Keep this repository private because application materials may contain personal information.

All job-specific resumes and cover letters must remain truthful. Do not fabricate experience, credentials, work authorization, qualifications, dates, or skills.
