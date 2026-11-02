# Redactions and Tree Pruning Log

This log documents files removed from the upstream repository (`adityash-ankar/Project_Svarog`) in this fork (`thomasvanpul/Project_Svarog`) prior to pushing.

## 1. Personal Identifiable Information (PII)
- **File:** `RXBX17_SNSA-ESA_CALL_ExperimentProposalForm_18Jun25.docx`
- **Location in Upstream:** Repository root
- **Reason for Removal:** Contains personal information of REXUS/BEXUS student team members in an unencrypted document (names, university affiliations, personal email addresses, phone numbers, and dates of birth for Piotr Fil, Aditya Shankar, and other student leads).
- **Disposition:** Removed from the git working tree and rewritten out of git commit history in this fork. The original document is archived safely in offline local project storage (`~/.atrium/svarog/original_unredacted/`).

## 2. Duplicate Document Files
- **Files:**
  - `Composite Booms/Academia/20170001569.pdf`
  - `Composite Booms/Academia/Fernandez - Advanced Deployable Shell-Based Composite Booms For Small Satellite Structural Applications Includin.pdf`
- **Reason for Removal:** Byte-identical copies of NASA/TM-2017-219665 (MD5: `898a313314a8791e92d94f01a92eeb6d`).
- **File:** `RX_UserManual_v7-17_26Nov21 (1).pdf`
- **Reason for Removal:** Third-party EuroLaunch document with browser duplicate suffix `(1)`. Replaced by reference in `references/references.md`.

## 3. Copyrighted Publisher PDFs
- **Location in Upstream:** `Composite Booms/Academia/` (12 PDF files, ~30 MB)
- **Reason for Removal:** Commercial journal articles (Elsevier, AIAA, Springer) distributed without open-access redistribution licensing in a public git repository.
- **Disposition:** Replaced with complete bibliographic metadata, DOIs, and direct links in `references/references.md`. Original reference files preserved in local developer cache.
