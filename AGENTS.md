# Job Application Preparation Agent Instructions

This repository is an on-demand job application preparation project for Amir Mirzai Golpayegani. These instructions are permanent operational rules for future Codex runs.

## Supported Commands

Use the local command infrastructure for all preparation work. Do not improvise the workflow manually.

- `./prepare next job`
- `./prepare job <Job Number>`
- `./prepare --dry-run next job`
- `./prepare --dry-run job <Job Number>`
- `./prepare finalize job <Job Number>`
- `./prepare add job <posting-url>`
- `./prepare --dry-run add job <posting-url>`

Natural-language user requests that match `prepare next job` or `prepare job <Job Number>` must invoke the matching local script. Process exactly one job per execution command.

Natural-language user requests that match `add job <posting-url>`, `add this job <posting-url>`, or `add <posting-url> to the sheet` must invoke `./prepare --dry-run add job <posting-url>` as a local preflight, then use the connected Google Drive/Sheets plugin to inspect and update the spreadsheet. Process exactly one posting URL per add command.

Do not prepare a real job during repository setup, review, refactoring, or testing unless the user explicitly issues one of the supported preparation commands.

Do not prepare application materials as part of `add job`. The add command only discovers, verifies, de-duplicates, scores, and records a posting as `Discovered`.

## Spreadsheet

Spreadsheet URL:

https://docs.google.com/spreadsheets/d/1FzeWuLeY0fv8uK3lGtNCY4QDfe0HbWq76bXY8moaqJs/edit?gid=1315930908#gid=1315930908

Spreadsheet ID:

`1FzeWuLeY0fv8uK3lGtNCY4QDfe0HbWq76bXY8moaqJs`

Worksheet tab:

`BotResults`

Expected columns, in order:

1. Job Number
2. Position Title
3. Company
4. Location
5. Priority
6. Fit Score
7. Status
8. Work Arrangement
9. Job Type
10. Posting Date
11. Date Added
12. Key Reasons for Fit
13. Main Gaps
14. Job ID
15. Salary
16. Expected Salary
17. Recruiter or Contact Person
18. LinkedIn Job Posting Link
19. Direct Application Link
20. Notes
21. Curated Resume PDF Link
22. Curated Resume LaTeX Link
23. Cover Letter PDF Link
24. Cover Letter LaTeX Link
25. Prepared Date
26. Errors

Valid status values are exactly:

- `Discovered`
- `Prepared`
- `Failed`

Status matching is exact. Do not treat differently capitalized or whitespace-padded values as equivalent without explicitly reporting the data issue.

Before selecting a row, verify the required column headers are present. Prefer header-based access over fixed column indices.

Before any spreadsheet write:

- re-read the selected row;
- confirm its Job Number is unchanged;
- confirm no other process has already changed its Status;
- confirm Position Title and Company are unchanged;
- update only the selected row;
- avoid overwriting unrelated columns.

## Expected Salary

`Expected Salary` is a preparation-time field. Leave it blank during discovery and manual job intake, then fill it when preparing the job.

When preparing a job, estimate a fair expected salary using the verified posting salary if available, the role level, location, work arrangement, market context, and Amir's qualifications. Do not underestimate Amir's value, because underrepresenting the candidate can weaken an application. Do not overreach beyond a defensible level either. Prefer a middle-to-upper-middle number or range that is ambitious but realistic for the specific role.

Use a concise numeric value only. Do not write a sentence. Use the posting currency when clearly stated; otherwise use CAD for Canadian roles. Examples: `CA$115,000` or `CA$105,000-CA$125,000`.

## Google Authentication

Use reliable programmatic Google Sheets access.

When running inside Codex, prefer the connected Google Drive/Sheets plugin for spreadsheet reads and writes. The plugin is the normal access path for this project because it uses the user's connected Google account and avoids storing local Google credentials in the repository.

Before relying on plugin writes, verify access with a safe read of the header row. For writes, use the plugin's spreadsheet batch update capability and follow the row re-read and status-update rules in this file.

Local Google credentials are only needed when running the standalone CLI outside Codex or when the Codex Google Drive plugin is unavailable.

Credentials must remain outside Git. Never commit OAuth client secrets, service-account JSON, refresh tokens, or complete credential logs.

Supported standalone local configuration:

- `JOBBOT_GOOGLE_SERVICE_ACCOUNT_FILE=/absolute/path/to/service-account.json`
- `JOBBOT_GOOGLE_AUTHORIZED_USER_FILE=/absolute/path/to/authorized-user.json`
- `JOBBOT_GOOGLE_TOKEN_FILE=/absolute/path/to/oauth-token.json`

The authenticated plugin account or standalone credential identity must have edit permission before any spreadsheet write.

## Repository And Sources

GitHub repository: `amirgolpaa24/JobApplicationBot`

Default branch: `main`

Authoritative master files:

- `master/Amir_Mirzai_Golpayegani_master_resume.tex`
- `master/Amir_Mirzai_Golpayegani_cover_letter_example.tex`

Authoritative GitHub Actions workflow:

- `.github/workflows/compile-latex.yml`

Do not overwrite, reformat, clean up, or modify the master files during ordinary job preparation. Treat them as sources of truth for truthful candidate claims and document structure.

## Output Structure

For Job Number `<number>`, use:

`applications/Job_<number>/`

Each completed job folder must contain:

- `applications/Job_<number>/resume.tex`
- `applications/Job_<number>/resume.pdf`
- `applications/Job_<number>/cover_letter.tex`
- `applications/Job_<number>/cover_letter.pdf`

Use the spreadsheet Job Number exactly in the folder name. Do not use external Job ID values for folder numbering. Do not create duplicate folders such as `Job_<number>_2`.

If a folder already exists, inspect its contents and classify it as partial, complete, or conflicting. Preserve valid existing files. Do not silently delete or overwrite completed work.

## Job Selection

For `prepare next job`:

- re-read the Google Sheet immediately;
- find rows whose Status is exactly `Discovered`;
- select one eligible row;
- sort by Priority first using `High`, then `Mid`, then `Low`, then blank or unrecognized values; within each priority group sort by Fit Score highest first, Date Added newest first, Posting Date newest first, then Job Number lowest first.

The `Priority` column is filled by the job match finder. Do not overwrite or infer it during preparation or manual job intake.

For `prepare job <Job Number>`:

- interpret the value as the spreadsheet Job Number, not a row number or external Job ID;
- re-read the spreadsheet immediately;
- find the exact matching row;
- do not substitute another job;
- if Status is not exactly `Discovered`, report the current Status and make no changes unless the user explicitly instructs otherwise.

## Manual Job Intake

For `add job <posting-url>`:

- treat the user-provided URL as the initial source of truth;
- accept either a LinkedIn job URL or an employer/company application URL;
- use the local add-job preflight first to validate that the command contains one supported URL;
- use the connected Google Drive/Sheets plugin for all live spreadsheet reads and writes when working inside Codex;
- do not add more than one spreadsheet row for a single user command;
- do not prepare a resume or cover letter.

Before writing a new row:

- read spreadsheet metadata and confirm the `BotResults` tab and expected headers;
- read the existing populated job rows;
- check for duplicates by normalized LinkedIn URL, normalized direct application URL, Job ID, and strong title/company match;
- if an existing row appears to represent the same posting, report the existing Job Number, Status, title, company, and matching evidence, then do not add a duplicate unless the user explicitly confirms;
- retrieve and verify the posting from the best available source, preferring the employer's direct application page when the user gave LinkedIn and the direct page can be found;
- verify the position title, company, location, work arrangement, job type, posting date or best available posting-age evidence, salary, recruiter/contact if present, Job ID if present, and whether the posting is still accessible;
- evaluate fit using Amir's master resume and truthful background only;
- assign the next Job Number as one greater than the maximum numeric Job Number already in the sheet;
- set Date Added in the user's local timezone;
- set Status exactly to `Discovered`;
- leave all preparation-only columns blank: Expected Salary, Curated Resume PDF Link, Curated Resume LaTeX Link, Cover Letter PDF Link, Cover Letter LaTeX Link, Prepared Date, and Errors;
- keep Notes concise and include any uncertainty about posting date, source reliability, or direct-link discovery.

The added row must fill these non-preparation columns when available or use `NA` when genuinely unavailable:

- Job Number
- Position Title
- Company
- Location
- Priority
- Fit Score
- Status
- Work Arrangement
- Job Type
- Posting Date
- Date Added
- Key Reasons for Fit
- Main Gaps
- Job ID
- Salary
- Recruiter or Contact Person
- LinkedIn Job Posting Link
- Direct Application Link
- Notes

After writing:

- re-read the new row;
- verify Job Number, Position Title, Company, Status, source links, Date Added, and blank preparation-only columns, including Expected Salary;
- report the added Job Number and the duplicate checks performed.

## Job Description Retrieval

Use the spreadsheet row as the initial source. Prefer the employer’s direct application link over LinkedIn or aggregators.

When retrieving a job description:

- verify Position Title;
- verify Company;
- verify Location;
- verify Job ID when available;
- verify the posting is accessible;
- record the source used;
- avoid similarly named but different positions.

If the complete description cannot be obtained but the row has enough reliable detail to tailor responsibly, explain the limitation before proceeding. If information is too thin to create a truthful package, treat it as a preparation failure.

## Hard Blockers

Default action is to prepare the application. Do not reject jobs merely because some preferred qualifications are missing.

Only these are hard blockers:

1. The posting is confirmed closed, removed, cancelled, or expired.
2. Canadian citizenship or permanent residency is explicitly mandatory.
3. Security clearance is mandatory and obtaining it explicitly requires citizenship or permanent residency Amir does not have.
4. Amir is confirmed legally ineligible to work in the required jurisdiction or under explicit posting requirements.
5. A mandatory regulated licence or professional certification is required and Amir does not possess it.
6. Mandatory work location or attendance requirements are genuinely incompatible with Amir’s situation.
7. Application files cannot be generated or compiled after reasonable troubleshooting.
8. The job description cannot be retrieved or verified sufficiently for a responsible package.

These are not hard blockers: missing preferred qualifications, fewer years than requested, preferred skills, learnable domain background, senior-sounding responsibilities in an attainable role, ordinary competition risk, lack of referral, or unconfirmed uncertainty.

Do not infer immigration ineligibility from sponsorship questions. Do not assume citizenship or permanent-residency requirements unless explicitly stated.

When a hard blocker is confirmed, do not prepare documents. Record the exact blocker in Errors. Set Status to `Failed` only when the blocker is confirmed and the workflow rules justify final failure; otherwise leave Status as `Discovered` and report manual review.

## Truthfulness

Documents must remain completely truthful.

Never fabricate or exaggerate years of experience, employment history, titles, responsibilities, languages, frameworks, cloud experience, certifications, academic credentials, immigration status, security clearance, publications, awards, projects, performance results, leadership, or industry experience.

Use only the master resume and other explicitly approved candidate sources in the repository. Do not add technologies solely because they appear in the job description. Do not convert academic exposure into professional employment experience. Present the strongest truthful match without apologizing for gaps.

## Resume Rules

Start from `master/Amir_Mirzai_Golpayegani_master_resume.tex`.

Keep the tailored resume recognizably based on the master. Unless explicitly approved, keep changes to approximately 10% to 20% of master content.

The following sections are protected and must always remain in every tailored resume:

- `Education`
- `Certificates`
- `Languages`
- `Achievement`

Do not remove, rename, or materially weaken protected sections during tailoring. Keep the factual degree details, certificate names, language proficiency, and achievements from the master resume unless the user explicitly approves a change.

Only these resume areas may be tailored for a job:

- `Summary`
- `Technical Skills`
- `Work Experience`
- `Research and Technical Projects`

Permitted tailoring in those areas includes section and bullet reordering, emphasizing supported skills, small truthful wording adjustments, lower-priority omissions for space, summary alignment, supported project selection, careful emphasis, and ATS alignment without keyword stuffing.

If page length is a concern, compile and inspect the actual page count before removing content. Do not guess based on source length. To reduce length, first trim or reorder lower-priority content inside the tailorable sections. Do not solve page-length issues by deleting protected sections.

Do not invent experience, rewrite so extensively that the resume no longer reflects the master, add unsupported technologies, change dates, change employers, inflate titles, change degree information, add fake metrics, or add claims derived only from the job description.

## Cover Letter Rules

Start from `master/Amir_Mirzai_Golpayegani_cover_letter_example.tex`.

Follow the example’s structure, tone, specificity, opening style, paragraph organization, closing style, and LaTeX formatting.

The cover letter must be tailored to the exact position and company, truthful, specific, one page, compilable, free of em dash characters, and free of invented hiring manager names.

Use a named recruiter or contact only when the spreadsheet or verified posting provides one. Otherwise use a general salutation.

## Local Validation

Before committing:

1. compile `resume.tex` locally with `latexmk`;
2. compile `cover_letter.tex` locally with `latexmk`;
3. confirm both commands exit successfully;
4. confirm both PDFs exist;
5. inspect page counts;
6. confirm the cover letter is one page;
7. check meaningful LaTeX warnings;
8. confirm no placeholders remain;
9. confirm job title and company are correct;
10. confirm no content from another application remains;
11. confirm no em dash exists in the cover letter;
12. confirm the tailored resume retains `Education`, `Certificates`, `Languages`, and `Achievement`;
13. confirm only truthful, supported claims are present.

Do not push LaTeX that fails local compilation when local LaTeX is available. Do not commit temporary compilation artifacts.

## Git And GitHub Workflow

For each selected job:

1. ensure local `main` is synchronized with `origin/main`;
2. ensure there are no unrelated uncommitted changes;
3. create or update only the selected job folder;
4. validate both LaTeX files locally;
5. inspect the diff;
6. stage only files belonging to the selected job;
7. commit clearly;
8. push to `main`;
9. record the commit SHA.

Suggested commit message:

`Prepare application for Job <Job Number>: <Position Title> at <Company>`

After pushing `.tex` files, identify the GitHub Actions run for the commit, wait for success, verify PDFs were committed, identify the PDF commit SHA, and verify all four remote files.

Do not assume a successful push means PDFs exist. Do not set Status to `Prepared` while Actions is pending.

## File Links And Spreadsheet Update

After all four files exist remotely, generate verified links for:

- Curated Resume PDF Link
- Curated Resume LaTeX Link
- Cover Letter PDF Link
- Cover Letter LaTeX Link

Prefer stable links tied to the final commit SHA. Ensure every link points to the selected Job Number.

Only after all four files exist remotely and links are verified, update the selected row:

- write Expected Salary as a concise number or range;
- write all four links;
- set Prepared Date in the user’s local timezone;
- clear stale resolved Errors;
- set Status exactly to `Prepared` last.

After writing, re-read the row and verify Expected Salary, links, Prepared Date, Errors, and Status.

## Failure, Idempotency, And Locking

A job is successful only when all four files exist remotely, links are verified and written to the correct spreadsheet row, Prepared Date is written, and Status is verified as `Prepared`.

On error, stop at the safest point, preserve valid work, avoid unrelated row updates, do not claim completion, and record a concise exact error.

The workflow must be safe to rerun. Before generating files, inspect the row, job folder, existing links, and relevant Git history. If files already exist and Status remains `Discovered`, verify and repair the spreadsheet state rather than regenerating unnecessarily.

Use a local lock so two preparation commands cannot operate on the same repository or spreadsheet row at once. The lock must identify the selected Job Number, avoid storing credentials, clean up after normal completion, and handle stale locks safely.

## Completion Report

After each preparation command, show a concise report with:

- command received;
- Job Number;
- Position Title;
- Company name;
- Location;
- Work Arrangement;
- Referral / Contact Person;
- Job Type;
- Expected Salary;
- selection reason for `prepare next job`;
- hard-blocker result;
- job-description source;
- files created or reused;
- local compilation results;
- resume page count;
- cover-letter page count;
- application commit SHA;
- PDF workflow status;
- PDF commit SHA when applicable;
- four final file links;
- final spreadsheet Status;
- Prepared Date;
- remaining error or manual action.

Do not report an unprocessed job as failed. Do not claim completion unless the spreadsheet row has been re-read and verified as `Prepared`.
