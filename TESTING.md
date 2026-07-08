# DevLens Testing Checklist

## Auth
- [x] Register works
- [x] Duplicate register is rejected
- [x] Login works
- [x] Invalid login is rejected
- [x] /auth/me works with token
- [x] /auth/me fails without token
- [x] Logout removes token

## Projects
- [x] Create project works
- [x] List projects works
- [x] Project detail opens
- [x] Other user cannot access project

## Upload and Scan
- [x] Valid zip upload works
- [x] Non-zip upload rejected
- [x] Corrupt zip fails safely
- [x] Scan status updates
- [x] Extracted repo exists
- [x] Ignored folders skipped

## Files
- [x] Files saved in DB
- [x] Tree loads
- [x] File detail loads
- [x] Content preview displays
- [x] Other user cannot access file

## AI
- [x] Chunks created
- [x] Embeddings generated
- [x] Summaries generated
- [x] Chat returns useful answer
- [x] Chat history persists

## Findings
- [x] TODO/FIXME detected
- [x] Secret-like pattern detected
- [x] Risky pattern detected
- [x] Missing tests hint works
- [x] Findings display in UI

## UI
- [x] Dashboard loads cleanly
- [x] Project page layout works
- [x] Loading states appear
- [x] Empty states appear
- [x] Error states appear