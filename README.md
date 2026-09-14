# Pseudo-Automation
Framework for doing automation driven manual testing

```
                 ┌── Selenium UI
                 │
Login ───────────┤
                 │
                 └── Authentication
                         │
                 cookies / tokens
                         │
                         ▼
                     ApiClient
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
             GET        POST       PUT
              │          │          │
              └──────────┼──────────┘
                         ▼
                    API assertions
```
