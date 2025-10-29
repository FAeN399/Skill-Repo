# Troubleshooting Template

## "[Error Message or Symptom 1]"

**Cause:** [Why this error occurs]

**Solution:**
1. [First troubleshooting step]
2. [Second step if first doesn't work]
3. [Final solution]

**Prevention:** [How to avoid this in the future]

---

## [Symptom-Based Issue]

**Symptoms:**
- [Observable behavior 1]
- [Observable behavior 2]

**Common Causes:**
1. [Cause 1] - Check with: `[diagnostic command]`
2. [Cause 2] - Verify: `[verification command]`

**Solutions:**
- **If cause 1:** [Solution steps]
- **If cause 2:** [Solution steps]

---

## Prerequisites Not Met

**Error:** [How it manifests]

**Required:**
- [Dependency 1] - Install with: `[command]`
- [Dependency 2] - Install with: `[command]`
- [Permission/access requirement]

**Verification:**
```bash
[command to verify prerequisites are met]
```

---

## Performance Issues

**Symptoms:**
- [What slow performance looks like]
- [When it happens]

**Solutions:**
1. **For large inputs:** [Optimization approach]
2. **For many files:** [Batch processing approach]
3. **Memory constraints:** [Memory-efficient alternative]

**Quick wins:**
- Use `--parallel` flag for multi-core processing
- Increase batch size: `--batch-size 1000`
- Filter early: `--filter "condition"` before processing

---

## Common Misconfigurations

### Issue: [Configuration Problem]

**Incorrect:**
```bash
[wrong command]
```

**Correct:**
```bash
[right command]
```

**Why:** [Explanation of the mistake]
