#!/usr/bin/env python3
"""
SYNRIX RAG Demo – Knowledge base style.

Ingest a support/docs-style corpus, then answer questions via semantic search.
Uses ~30 built-in docs (many >512 bytes → chunked storage).

Requires: synrix_rag package. Run with SYNRIX_LIB_PATH set:
  cd python-sdk && pip install -e . && python examples/rag_demo_kb.py
"""

import os
import sys
import time

_script_dir = os.path.dirname(os.path.abspath(__file__))
_sdk_root = os.path.dirname(_script_dir)
if _sdk_root not in sys.path:
    sys.path.insert(0, _sdk_root)

KB_DOCS = [
    ("Password reset", "How to reset your password. If you forgot your password, go to the login page and click Forgot password. Enter your email and we will send a secure link valid for 24 hours. Do not share this link. If you use SSO, contact your IT admin to reset your password. For security we lock accounts after 5 failed attempts for 15 minutes. To unlock earlier, use the same Forgot password flow or contact support. If you do not receive the email within a few minutes, check your spam folder and ensure you entered the correct address. Password requirements: at least 8 characters, including one number and one symbol. You can change your password anytime from Account -> Security."),
    ("Refund policy", "Refunds are available within 30 days of purchase for annual plans. Monthly plans can be cancelled anytime; no refund for the current month. To request a refund go to Billing in the dashboard, select the invoice, and click Request refund. Refunds are processed within 5–10 business days to the original payment method. Enterprise contracts are governed by the signed agreement; contact your account manager for cancellation terms."),
    ("API rate limits", "API rate limits depend on your plan. Free: 100 requests per minute. Pro: 1000 per minute. Enterprise: configurable. When you exceed the limit you receive HTTP 429; the Retry-After header indicates when to retry. We recommend exponential backoff. For bulk operations use our batch endpoints which count as a single request. Rate limits are per API key and per endpoint; contact us for higher limits."),
    ("Two-factor authentication", "We support 2FA via TOTP (authenticator apps like Google Authenticator or Authy). Enable 2FA in Account → Security. Scan the QR code with your app and enter the code to confirm. Save your backup codes in a safe place; you will need one if you lose your device. Recovery can take 24–48 hours if you lose both device and backup codes. SSO users may have 2FA enforced by their identity provider."),
    ("Exporting your data", "You can export all your data from Settings → Data export. Exports include projects, history, and assets in a ZIP. Large accounts may take up to 24 hours; we email you when the export is ready. Exports are available for 7 days. For GDPR or legal hold we can provide a full backup; contact support with your request and we will respond within 5 business days."),
    ("Billing and invoices", "Invoices are generated at the start of each billing cycle. You can download them from Billing → Invoices. We accept major credit cards and ACH (US). Enterprise customers can pay by invoice (NET 30). Update your payment method anytime in Billing. Failed payments trigger 3 retry attempts; we notify you by email. If payment continues to fail, your account may be restricted until the balance is paid."),
    ("SSO and SAML", "Enterprise plans can enable SAML 2.0 SSO. Configure your IdP with our SAML metadata URL (found in Settings → SSO). We support Okta, Azure AD, Google Workspace, and any SAML 2.0–compliant provider. After SSO is enabled, users sign in through your IdP. Just-in-time provisioning is supported; we create user records on first sign-in. Contact your account manager to enable SSO."),
    ("Webhook setup", "Webhooks notify your server when events occur (e.g. run completed, model trained). Create a webhook in Settings → Integrations: add the URL and choose events. We sign payloads with HMAC-SHA256; verify the X-Signature header. We retry failed deliveries with exponential backoff for up to 24 hours. Respond with 2xx quickly to avoid retries. For high volume we recommend our event stream API instead."),
    ("Database connection limits", "Each plan has a maximum number of concurrent database connections. Free: 5, Pro: 25, Enterprise: 100 or custom. Connections are pooled; idle connections are released after 10 minutes. If you hit the limit you will see Too many connections. Reduce connection lifetime in your client or upgrade your plan. For read replicas, connections are counted per replica."),
    ("Troubleshooting slow queries", "Slow queries are usually due to missing indexes or large scans. Use the Query analyzer in the dashboard to see execution plans. Add indexes on frequently filtered or joined columns. Avoid SELECT *; fetch only needed columns. For analytics, use our batch query API which runs during off-peak hours. If the issue persists, our support team can review your schema and suggest optimizations."),
    ("Backup and recovery", "We take automated daily backups of your data. Backups are retained for 30 days on Pro and 90 days on Enterprise. Point-in-time recovery is available for the last 7 days. To restore, contact support with the desired timestamp; we will restore to a new environment for you to verify before switching. Self-service restore is available on Enterprise via the dashboard."),
    ("Compliance and SOC 2", "We are SOC 2 Type II certified. Our compliance documentation and penetration test summaries are available under NDA for Enterprise customers. We support data residency in US and EU. For HIPAA we offer a BAA on Enterprise; for GDPR we provide DPA and process data per our privacy policy. Audit logs are available in the dashboard for 90 days (longer on request)."),
    ("Getting started guide", "Welcome. After signup, create a project and invite your team from Settings → Members. Install the CLI with the one-liner from the dashboard; use it to run jobs and sync config. Our docs and tutorials are in the Help menu. For a guided tour, click your profile and select Product tour. Need help? Use the in-app chat or email support@example.com. Community forum and status page are linked in the footer."),
    ("Keyboard shortcuts", "Quick reference: Ctrl+K or Cmd+K for command palette. Ctrl+/ for keyboard shortcuts help. In the editor: Ctrl+S to save, Ctrl+Enter to run. In the file tree: Ctrl+N new file, Ctrl+Shift+N new folder. We support custom shortcuts in Settings → Shortcuts. Most actions are available from the command palette; type to search."),
    ("Contacting support", "Free users can use the community forum and docs. Pro and Enterprise get email support; response time is within 24 hours for Pro and 4 hours for Enterprise. Include your account email and a clear description. For outages use the in-app priority channel. Enterprise has a dedicated success manager and optional premium support with a guaranteed response time."),
]

QUERIES = [
    "How do I reset my password?",
    "What is your refund policy?",
    "API rate limits and 429 errors",
    "How to set up two-factor authentication",
    "Export my data or get a backup",
    "Where do I find my invoices?",
]


def main():
    demo_lattice = os.path.join(_script_dir, "demo_kb.lattice")
    if os.path.exists(demo_lattice):
        try:
            os.remove(demo_lattice)
        except Exception:
            pass

    print("SYNRIX RAG Demo – Knowledge base")
    print("=================================\n")

    synrix_client = None
    try:
        from synrix.ai_memory import AIMemory
        synrix_client = AIMemory(lattice_path=demo_lattice)
        print("[OK] SYNRIX backend.\n")
    except ImportError:
        print("[WARN] synrix not installed; using in-memory fallback.\n")
    except Exception as e:
        print(f"[WARN] SYNRIX init failed: {e}; using in-memory fallback.\n")

    from synrix_rag import RAGMemory

    rag = RAGMemory(
        collection_name="support_kb",
        embedding_model="local",
        synrix_client=synrix_client,
    )

    total_chars = 0
    chunked_count = 0
    t0 = time.perf_counter()
    print(f"Ingesting {len(KB_DOCS)} documents...")
    for title, text in KB_DOCS:
        doc_id = rag.add_document(text=text, metadata={"title": title})
        size = len(text.encode("utf-8"))
        total_chars += size
        if size > 511:
            chunked_count += 1
    ingest_time = time.perf_counter() - t0
    print(f"   Done in {ingest_time:.2f}s ({len(KB_DOCS)} docs, {total_chars:,} chars, {chunked_count} chunked).\n")

    print("Sample queries:\n")
    for q in QUERIES[:4]:
        t0 = time.perf_counter()
        results = rag.search(q, top_k=2)
        elapsed = time.perf_counter() - t0
        top = results[0] if results else {}
        title = top.get("metadata", {}).get("title", "-")
        score = top.get("score", 0)
        print(f"   Q: {q}")
        print(f"   -> Top: \"{title}\" (score={score:.3f}, {elapsed*1000:.0f}ms)\n")

    ctx = rag.get_context("How do I get a refund?", top_k=2)
    print("Context for LLM:", ctx[:400] + "...\n")
    print("Demo complete.")
    if synrix_client and os.path.exists(demo_lattice):
        print(f"Lattice: {demo_lattice}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
