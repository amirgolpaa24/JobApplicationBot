# JobApplicationBot

This repository stores the LaTeX sources and generated PDFs for an automated job-application workflow. It is intended to keep reusable master documents separate from job-specific application packages, while GitHub Actions handles PDF compilation.

## Master Documents

The `master/` directory contains the reusable source documents:

- `master/Amir_Mirzai_Golpayegani_master_resume.tex`
- `master/Amir_Mirzai_Golpayegani_cover_letter_example.tex`

These files are the starting point for tailored applications. The current files may be placeholders; replace them with the real master LaTeX content before generating production applications.

## Application Folders

Each job application should live in its own numbered folder:

```text
applications/
└── Job_<job_number>/
    ├── resume.tex
    ├── resume.pdf
    ├── cover_letter.tex
    ├── cover_letter.pdf
    └── metadata.json
```

Use one folder per application. Keep the job-specific `resume.tex`, `cover_letter.tex`, generated PDFs, and metadata together so each application can be audited later.

Recommended `metadata.json` format:

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

## LaTeX Compilation

The workflow at `.github/workflows/compile-latex.yml` compiles job-specific LaTeX files in GitHub Actions. It runs on Ubuntu when:

- changes are pushed to `main` under `applications/**/*.tex`
- the workflow file itself changes
- the workflow is started manually with `workflow_dispatch`

For every `applications/Job_*` directory, the workflow compiles `resume.tex` and `cover_letter.tex` when those files exist. Compilation runs from inside each job folder with `latexmk -pdf`, so generated PDFs remain beside their source files.

After a successful run, auxiliary LaTeX files are removed and only newly generated or updated PDFs are committed back to the same branch. If compilation succeeds but no PDFs changed, the workflow exits successfully without creating a commit.

PDF-only commits do not retrigger the workflow because the push trigger only watches `.tex` sources and the workflow YAML file.

## Manual Workflow Runs

To trigger compilation manually:

1. Open the repository on GitHub.
2. Go to the **Actions** tab.
3. Select **Compile LaTeX applications**.
4. Choose **Run workflow** on the `main` branch.

## Failed Compilations

If compilation fails, open the failed run in the **Actions** tab and inspect the log for the relevant job folder and source file. The workflow uses `-halt-on-error`, so the first LaTeX error should appear near the end of the failed compilation output.

## Privacy And Truthfulness

This repository should remain private because resumes, cover letters, and metadata can contain personal information and sensitive job-search details.

Job-specific resumes and cover letters must remain truthful. Do not fabricate experience, qualifications, work authorization, credentials, dates, employers, education, or skills.
