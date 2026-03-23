// Set active navigation link based on current page
document.addEventListener('DOMContentLoaded', function() {
  const currentPage = window.location.pathname.split('/').pop() || '/';
  const navLinks = document.querySelectorAll('nav a');
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === '/')) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  // Show welcome message on home page if user is logged in
  if (currentPage === '/' || currentPage === '') {
    const userName = localStorage.getItem('authenticheck_user_name');
    const welcomeDiv = document.getElementById('welcome-user');
    if (welcomeDiv) {
      if (userName) {
        welcomeDiv.textContent = `Welcome, ${userName}!`;
        welcomeDiv.style.margin = '1.5rem 0 0 0';
        welcomeDiv.style.fontSize = '1.3rem';
        welcomeDiv.style.fontWeight = '600';
        welcomeDiv.style.color = '#2563eb';
      } else {
        welcomeDiv.textContent = '';
      }
    }
  }

  // Google sign-in demo handler for both register and login pages
  function handleGoogleSignIn() {
    // Simulate Google OAuth: set demo user and redirect
    localStorage.setItem('authenticheck_user_name', 'GoogleUser');
    window.location.href = '/';
  }
  // Attach to register page
  const googleRegisterBtn = document.getElementById('google-register-btn');
  if (googleRegisterBtn) {
    googleRegisterBtn.addEventListener('click', function(e) {
      e.preventDefault();
      handleGoogleSignIn();
    });
  }
  // Attach to login page
  const googleLoginBtn = document.getElementById('google-login-btn');
  if (googleLoginBtn) {
    googleLoginBtn.addEventListener('click', function(e) {
      e.preventDefault();
      handleGoogleSignIn();
    });
  }
});

// Client-side cache and timers for stored documents
var storedDocsCache = [];
var storedAutoRefreshTimer = null;
var storedSearchDebounce = null;

// Client-side cache and timers for uploaded documents
var uploadedDocsCache = [];
var uploadedAutoRefreshTimer = null;
var uploadedSearchDebounce = null;
// Handle login and register form submissions to store user name and redirect to home
document.addEventListener('DOMContentLoaded', function() {
  // Register form
  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const nameInput = registerForm.querySelector('input[type="text"]');
      const userName = nameInput ? nameInput.value.trim() : '';
      if (userName) {
        localStorage.setItem('authenticheck_user_name', userName);
      }
      window.location.href = '/';
    });
  }
  // Login form
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      // For demo, just use email as user name
      const emailInput = loginForm.querySelector('input[type="email"]');
      let userName = '';
      if (emailInput) {
        userName = emailInput.value.split('@')[0];
      }
      if (userName) {
        localStorage.setItem('authenticheck_user_name', userName);
      }
      window.location.href = '/';
    });
  }
});

// Mini message popup (no action buttons)
function showMiniPopup(message) {
  const existingContainer = document.getElementById('miniPopupContainer');
  const container = existingContainer || (() => {
    const c = document.createElement('div');
    c.id = 'miniPopupContainer';
    c.style.position = 'fixed';
    c.style.top = '1rem';
    c.style.right = '1rem';
    c.style.zIndex = '9999';
    c.style.display = 'flex';
    c.style.flexDirection = 'column';
    c.style.gap = '0.5rem';
    c.style.maxWidth = '320px';
    document.body.appendChild(c);
    return c;
  })();

  const popup = document.createElement('div');
  popup.textContent = message;
  popup.style.background = '#111827';
  popup.style.color = '#ffffff';
  popup.style.padding = '0.6rem 0.8rem';
  popup.style.borderRadius = '8px';
  popup.style.fontSize = '0.9rem';
  popup.style.lineHeight = '1.35';
  popup.style.boxShadow = '0 8px 20px rgba(0,0,0,0.25)';
  popup.style.opacity = '0';
  popup.style.transform = 'translateY(-6px)';
  popup.style.transition = 'opacity 180ms ease, transform 180ms ease';

  container.appendChild(popup);
  requestAnimationFrame(() => {
    popup.style.opacity = '1';
    popup.style.transform = 'translateY(0)';
  });

  setTimeout(() => {
    popup.style.opacity = '0';
    popup.style.transform = 'translateY(-6px)';
    setTimeout(() => {
      if (popup.parentNode) popup.parentNode.removeChild(popup);
      if (container.childElementCount === 0 && container.parentNode) {
        container.parentNode.removeChild(container);
      }
    }, 180);
  }, 2600);
}

// Document verification handler for upload.html
// Drag-and-drop and progress logic for upload.html
document.addEventListener('DOMContentLoaded', function() {
  const dragDropArea = document.getElementById('dragDropArea');
  const hiddenFileInput = document.getElementById('docFile');
  const formFileInput = document.getElementById('docFileForm');
  const uploadProgress = document.getElementById('uploadProgress');
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');

  if (dragDropArea && hiddenFileInput && formFileInput) {
    dragDropArea.addEventListener('click', () => hiddenFileInput.click());
    dragDropArea.addEventListener('dragover', e => {
      e.preventDefault();
      dragDropArea.style.background = '#e0e7ff';
      dragDropArea.style.borderColor = '#2563eb';
    });
    dragDropArea.addEventListener('dragleave', e => {
      e.preventDefault();
      dragDropArea.style.background = '#f0f6ff';
      dragDropArea.style.borderColor = '#3b82f6';
    });
    dragDropArea.addEventListener('drop', e => {
      e.preventDefault();
      dragDropArea.style.background = '#f0f6ff';
      dragDropArea.style.borderColor = '#3b82f6';
      if (e.dataTransfer.files.length > 0) {
        hiddenFileInput.files = e.dataTransfer.files;
        formFileInput.files = e.dataTransfer.files;
        showMiniPopup('File added!');
      }
    });
    hiddenFileInput.addEventListener('change', () => {
      formFileInput.files = hiddenFileInput.files;
    });
    formFileInput.addEventListener('change', () => {
      hiddenFileInput.files = formFileInput.files;
    });
  }
});

  window.handleVerifyAuthenticity = async function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('docFileForm');
    if (!fileInput || fileInput.files.length === 0) {
      showMiniPopup('Please select a document to upload.');
      return;
    }
    // Show progress bar
    const uploadProgress = document.getElementById('uploadProgress');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    if (uploadProgress && progressBar && progressText) {
      uploadProgress.style.display = 'block';
      progressBar.style.width = '0%';
      progressText.textContent = 'Uploading...';
    }
    const formData = new FormData();
    formData.append('docFileForm', fileInput.files[0]);
    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
        credentials: 'same-origin'
      });
      if (uploadProgress && progressBar && progressText) {
        progressBar.style.width = '100%';
        progressText.textContent = 'Upload complete! Verifying...';
      }
      if (response.redirected) {
        window.location.href = response.url;
        return;
      }
      const text = await response.text();
      if (text.includes('report')) {
        window.location.href = '/report';
      } else {
        showMiniPopup('Upload failed. Please try again.');
        if (uploadProgress) uploadProgress.style.display = 'none';
      }
    } catch (err) {
      showMiniPopup('Error uploading file.');
      if (uploadProgress) uploadProgress.style.display = 'none';
    }
  }

// Display and simulate verification results
function showVerificationResults(file) {
  try {
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'block';

    // Update document information with error logging
    try { document.getElementById('resultFileName').textContent = file.name; } catch(e) { console.error('Missing #resultFileName', e); }
    try { document.getElementById('resultFileType').textContent = 'Academic Document'; } catch(e) { console.error('Missing #resultFileType', e); }
    try { document.getElementById('resultFileSize').textContent = (file.size / 1024).toFixed(2) + ' KB'; } catch(e) { console.error('Missing #resultFileSize', e); }
    try { document.getElementById('resultUploadTime').textContent = new Date().toLocaleString(); } catch(e) { console.error('Missing #resultUploadTime', e); }

    // Reset status message
    try { document.getElementById('statusMessage').textContent = 'Verification in progress...'; } catch(e) { console.error('Missing #statusMessage', e); }

    // Simulate verification process
    setTimeout(function() {
      simulateVerification(file);
    }, 1500);

    // Scroll to result section
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    console.error('Error in showVerificationResults:', err);
    showMiniPopup('Error displaying verification results. See console for details.');
  }
}

// Simulate document verification process
function simulateVerification(file) {
  // Generate verification results with smart fake detection
  const verificationResults = generateMockResults(file);
  

  // Update plagiarism detection results with error logging
  try { document.getElementById('resultPlagiarism').textContent = verificationResults.plagiarismScore + '%'; } catch(e) { console.error('Missing #resultPlagiarism', e); }
  try { document.getElementById('resultPlagiarism').style.color = verificationResults.plagiarismScore > 20 ? '#ef4444' : '#10b981'; } catch(e) {}
  try { document.getElementById('resultMatchedContent').innerHTML = verificationResults.plagiarismScore > 20 
    ? `<i class="fas fa-exclamation-circle"></i> High - ${verificationResults.plagiarismScore}% copied content`
    : `<i class="fas fa-check-circle"></i> Very Low - ${verificationResults.plagiarismScore}%`; } catch(e) { console.error('Missing #resultMatchedContent', e); }
  try { document.getElementById('resultMatchedContent').style.color = verificationResults.plagiarismScore > 20 ? '#ef4444' : '#10b981'; } catch(e) {}
  try { document.getElementById('resultSourceDetection').innerHTML = verificationResults.plagiarismScore > 20
    ? `<i class="fas fa-times-circle"></i> Multiple suspicious sources found`
    : `<i class="fas fa-check-circle"></i> Educational databases (${verificationResults.plagiarismScore}%)`; } catch(e) { console.error('Missing #resultSourceDetection', e); }
  try { document.getElementById('resultSourceDetection').style.color = verificationResults.plagiarismScore > 20 ? '#ef4444' : '#10b981'; } catch(e) {}

  // Update paraphrasing detection results
  try { document.getElementById('resultParaphrasing').textContent = verificationResults.paraphrasingScore + '%'; } catch(e) { console.error('Missing #resultParaphrasing', e); }
  try { document.getElementById('resultParaphrasing').style.color = verificationResults.paraphrasingScore > 25 ? '#ef4444' : '#10b981'; } catch(e) {}
  try { document.getElementById('resultSimilarPhrases').innerHTML = verificationResults.paraphrasingScore > 25
    ? `<i class="fas fa-exclamation-circle"></i> ${Math.floor(verificationResults.paraphrasingScore / 10)} clusters - Suspicious rewriting`
    : `<i class="fas fa-check-circle"></i> 1 cluster - Natural language`; } catch(e) { console.error('Missing #resultSimilarPhrases', e); }
  try { document.getElementById('resultSimilarPhrases').style.color = verificationResults.paraphrasingScore > 25 ? '#ef4444' : '#10b981'; } catch(e) {}
  try { document.getElementById('resultSemanticSimilarity').innerHTML = verificationResults.paraphrasingScore > 25
    ? `<i class="fas fa-exclamation-circle"></i> ${verificationResults.paraphrasingScore}% - High Similarity`
    : `<i class="fas fa-check-circle"></i> ${verificationResults.paraphrasingScore}% - Very Low`; } catch(e) { console.error('Missing #resultSemanticSimilarity', e); }
  try { document.getElementById('resultSemanticSimilarity').style.color = verificationResults.paraphrasingScore > 25 ? '#ef4444' : '#10b981'; } catch(e) {}

  // Update tampering detection results
  try { document.getElementById('resultIntegrity').innerHTML = !verificationResults.isAuthentic
    ? `<i class="fas fa-exclamation-triangle"></i> COMPROMISED - Tampering Detected`
    : `<i class="fas fa-check-circle"></i> INTACT - No Tampering`; } catch(e) { console.error('Missing #resultIntegrity', e); }
  try { document.getElementById('resultIntegrity').style.color = verificationResults.integrityColor; } catch(e) {}
  try { document.getElementById('resultMetadata').innerHTML = !verificationResults.isAuthentic
    ? `<i class="fas fa-exclamation-circle"></i> ${50 + Math.random() * 30 | 0}% - Inconsistent/Missing`
    : `<i class="fas fa-check-circle"></i> 98% - Consistent`; } catch(e) { console.error('Missing #resultMetadata', e); }
  try { document.getElementById('resultMetadata').style.color = verificationResults.metadataColor; } catch(e) {}
  try { document.getElementById('resultForgery').innerHTML = `<i class="fas fa-${!verificationResults.isAuthentic ? 'times-circle' : 'check-circle'}"></i> ${verificationResults.forgery}`; } catch(e) { console.error('Missing #resultForgery', e); }
  try { document.getElementById('resultForgery').style.color = verificationResults.forgeryColor; } catch(e) {}

  // Update authorship analysis
  try { document.getElementById('resultAuthorMatch').innerHTML = !verificationResults.isAuthentic
    ? `<i class="fas fa-times-circle"></i> FAILED - Author Mismatch`
    : `<i class="fas fa-check-circle"></i> VERIFIED`; } catch(e) { console.error('Missing #resultAuthorMatch', e); }
  try { document.getElementById('resultAuthorMatch').style.color = verificationResults.isAuthentic ? '#10b981' : '#ef4444'; } catch(e) {}
  try { document.getElementById('resultWritingStyle').innerHTML = !verificationResults.isAuthentic
    ? `<i class="fas fa-exclamation-circle"></i> ${40 + Math.random() * 30 | 0}% - Inconsistent`
    : `<i class="fas fa-check-circle"></i> 91% - Very Consistent`; } catch(e) { console.error('Missing #resultWritingStyle', e); }
  try { document.getElementById('resultWritingStyle').style.color = verificationResults.isAuthentic ? '#10b981' : '#ef4444'; } catch(e) {}
  try { document.getElementById('resultLinguisticPattern').innerHTML = !verificationResults.isAuthentic
    ? `<i class="fas fa-exclamation-circle"></i> ${35 + Math.random() * 40 | 0}% - Suspicious Pattern`
    : `<i class="fas fa-check-circle"></i> 89% - High Consistency`; } catch(e) { console.error('Missing #resultLinguisticPattern', e); }
  try { document.getElementById('resultLinguisticPattern').style.color = verificationResults.isAuthentic ? '#10b981' : '#ef4444'; } catch(e) {}

  // Update overall result
  let statusBadge;
  try { statusBadge = document.getElementById('statusBadge'); } catch(e) { console.error('Missing #statusBadge', e); }
  const isAuthentic = verificationResults.isAuthentic;
  try {
    if (isAuthentic && statusBadge) {
      statusBadge.textContent = '✓ ORIGINAL';
      statusBadge.style.color = '#10b981';
      document.getElementById('overallResult').style.background = '#d1fae5';
      document.getElementById('overallResult').style.borderLeft = '5px solid #10b981';
    } else if (statusBadge) {
      statusBadge.textContent = '✗ FAKE/FORGED DETECTED';
      statusBadge.style.color = '#ef4444';
      document.getElementById('overallResult').style.background = '#fee2e2';
      document.getElementById('overallResult').style.borderLeft = '5px solid #ef4444';
    }
  } catch(e) { console.error('Missing #overallResult or #statusBadge', e); }

  // concise summary: ORIGINAL or EDITED
  let resultSummaryEl;
  try { resultSummaryEl = document.getElementById('resultSummary'); } catch(e) { console.error('Missing #resultSummary', e); }
  try {
    if (resultSummaryEl) {
      if (isAuthentic) {
        resultSummaryEl.textContent = 'ORIGINAL';
        resultSummaryEl.style.color = '#065f46';
      } else {
        resultSummaryEl.textContent = 'EDITED';
        resultSummaryEl.style.color = '#7f1d1d';
      }
    }
  } catch(e) {}

  try { document.getElementById('confidenceScore').innerHTML = 
    `<i class="fas fa-poll"></i> Confidence Score: <span style="font-weight: bold; font-size: 1.1rem; color: ${isAuthentic ? '#10b981' : '#ef4444'};">${verificationResults.confidence}%</span>`; } catch(e) { console.error('Missing #confidenceScore', e); }

  // Update report text (if element exists)
  try {
    const resultReportEl = document.getElementById('resultReport');
    if (resultReportEl) resultReportEl.textContent = verificationResults.report;
  } catch(e) { console.error('Missing #resultReport', e); }

  // Update overall message paragraph (fixed: was static in HTML and caused contradictory UI)
  try {
    const overallMessageEl = document.getElementById('overallMessage');
    if (overallMessageEl) {
      if (isAuthentic) {
        overallMessageEl.innerHTML = '<i class="fas fa-info-circle"></i> All verification checks passed successfully. Document is authentic and original.';
        overallMessageEl.style.color = '#065f46';
      } else {
        overallMessageEl.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Verification has flagged potential issues.';
        overallMessageEl.style.color = '#7f1d1d';
      }
    }
  } catch(e) { console.error('Missing #overallMessage', e); }

  // Update status message
  try {
    document.getElementById('statusMessage').innerHTML = 
      isAuthentic 
        ? '<span style="color: #10b981; font-weight: bold;"><i class="fas fa-check-circle"></i> Document verification completed - Authentic</span>'
        : '<span style="color: #ef4444; font-weight: bold;"><i class="fas fa-exclamation-triangle"></i> Document verification completed - FAKE/FORGED DETECTED</span>';
  } catch(e) { console.error('Missing #statusMessage', e); }

  // Display suspicious content if found (guarded)
  try {
    const suspiciousSection = document.getElementById('suspiciousContentSection');
    if (suspiciousSection) {
      if (!isAuthentic && verificationResults.suspiciousContent.length > 0) {
        suspiciousSection.style.display = 'block';

        let contentHTML = '';
        verificationResults.suspiciousContent.forEach((item, index) => {
          contentHTML += `
            <div style="margin-bottom: 1.5rem; padding: 1rem; background: white; border-left: 4px solid ${item.color}; border-radius: 4px;">
              <p style="margin: 0 0 0.5rem 0; font-weight: bold; color: ${item.color};">
                <i class="fas fa-${item.type === 'PLAGIARISM' ? 'copy' : item.type === 'PARAPHRASING' ? 'pen-fancy' : item.type === 'FORGERY DETECTION' ? 'exclamation-triangle' : 'user-check'}"></i>
                ${item.type} - ${item.percentage}% Match
              </p>
              <p style="margin: 0.3rem 0; color: #7f1d1d; font-size: 0.9rem;">
                <strong>Location:</strong> ${item.location}
              </p>
              <p style="margin: 0.3rem 0; color: #7f1d1d; font-size: 0.9rem;">
                <strong>Issue:</strong> ${item.issue}
              </p>
              <p style="margin: 0.5rem 0 0 0; padding: 0.8rem; background: #fef3c7; border-radius: 4px; border-left: 3px solid ${item.color}; color: #7f1d1d; font-size: 0.9rem; font-style: italic;">
                <i class="fas fa-quote-left" style="margin-right: 0.5rem; color: ${item.color};"></i>
                ${item.content}
                <i class="fas fa-quote-right" style="margin-left: 0.5rem; color: ${item.color};"></i>
              </p>
            </div>
          `;
        });

        const suspiciousListEl = document.getElementById('suspiciousContentList');
        if (suspiciousListEl) suspiciousListEl.innerHTML = contentHTML;
      } else {
        suspiciousSection.style.display = 'none';
      }
    }
  } catch(e) { console.error('Missing #suspiciousContentSection or #suspiciousContentList', e); }

  // Automatically save verified document to database
  // Save suspicious findings globally for upload
  window.lastSuspiciousFindings = verificationResults.suspiciousContent || [];
  uploadToDB();
}

// Generate mock verification results with smart fake document detection
function generateMockResults(file) {
  const fileName = file.name.toLowerCase();
  const fileSize = file.size;
  const type = file.type;
  
  // Detection logic for fake documents
  let isSuspicious = false;
  let suspicionReasons = [];
  let suspiciousContent = [];
  
  // Check for extremely small files (likely fake/empty)
  if (fileSize < 5000) {
    isSuspicious = true;
    suspicionReasons.push('File size abnormally small for academic document');
  }
  
  // Check for suspicious file extensions
  if (fileName.includes('fake') || fileName.includes('copy') || fileName.includes('duplicate')) {
    isSuspicious = true;
    suspicionReasons.push('Suspicious file naming pattern detected');
  }
  
  // Check for mismatching file extensions and MIME types
  if (fileName.endsWith('.pdf') && type !== 'application/pdf' && type !== '') {
    isSuspicious = true;
    suspicionReasons.push('File extension does not match actual file type');
  }
  
  // Check for unusual file sizes (too large for a single document)
  if (fileSize > 100 * 1024 * 1024) {
    isSuspicious = true;
    suspicionReasons.push('File size suspiciously large for single document');
  }
  
  // Deterministic detection: remove random false-positive factor
  const isAuthentic = !isSuspicious;
  // Confidence: higher when authentic, moderate when suspicious
  const confidence = isAuthentic
    ? Math.floor(Math.random() * 5 + 95)  // 95-99 for authentic
    : Math.floor(Math.random() * 20 + 40); // 40-59 for suspicious

  // Determine plagiarism/paraphrasing levels based on explicit suspicion
  const plagiarismScore = isAuthentic ? Math.floor(Math.random() * 6 + 2) : Math.floor(Math.random() * 40 + 30);
  const paraphrasingScore = isAuthentic ? Math.floor(Math.random() * 6 + 5) : Math.floor(Math.random() * 45 + 30);
  
  // Generate suspicious content examples only when explicit issues detected
  if (!isAuthentic) {
    // Plagiarism findings (based on score)
    if (plagiarismScore > 20) {
      suspiciousContent.push({
        type: 'PLAGIARISM',
        location: 'Detected sections',
        issue: 'Significant overlap with known sources',
        content: 'Portions of the document match content available in public sources',
        percentage: plagiarismScore,
        color: '#ef4444'
      });
    }

    // Paraphrasing findings (based on score)
    if (paraphrasingScore > 25) {
      suspiciousContent.push({
        type: 'PARAPHRASING',
        location: 'Detected sections',
        issue: 'Rewritten content closely mirrors published work',
        content: 'Detected paraphrased passages with high semantic similarity',
        percentage: paraphrasingScore,
        color: '#f59e0b'
      });
    }

    // Forgery detection findings: add only if filename/metadata checks indicated issues
    if (suspicionReasons.length > 0 && (suspicionReasons.includes('Suspicious file naming pattern detected') || suspicionReasons.includes('File extension does not match actual file type') || suspicionReasons.includes('File size abnormally small for academic document'))) {
      suspiciousContent.push({
        type: 'FORGERY DETECTION',
        location: 'Signature Block & Metadata',
        issue: 'Digital signature missing or metadata inconsistent',
        content: 'Signature or metadata checks failed based on file properties',
        percentage: 92,
        color: '#ef4444'
      });
    }

    // Authorship analysis: only when clear inconsistency detected
    if (suspicionReasons.length > 0 && suspicionReasons.some(r => r.toLowerCase().includes('suspicious'))) {
      suspiciousContent.push({
        type: 'AUTHORSHIP ANALYSIS',
        location: 'Document sections',
        issue: 'Writing style inconsistency detected',
        content: 'Sections of the document show inconsistent writing style',
        percentage: 80,
        color: '#f59e0b'
      });
    }
  }
  
  const results = {
    isAuthentic: isAuthentic,
    confidence: confidence,
    plagiarismScore: plagiarismScore,
    paraphrasingScore: paraphrasingScore,
    suspiciousContent: suspiciousContent,
    signature: isAuthentic ? 'Valid' : 'Not Found / Invalid',
    signatureColor: isAuthentic ? '#27ae60' : '#e74c3c',
    integrity: isAuthentic ? 'Verified - No Tampering' : 'Compromised - Alterations Detected',
    integrityColor: isAuthentic ? '#27ae60' : '#e74c3c',
    metadata: isAuthentic ? 'Complete & Consistent' : 'Missing / Inconsistent',
    metadataColor: isAuthentic ? '#27ae60' : '#e74c3c',
    forgery: isAuthentic ? 'No Signs Detected' : 'Potential Forgery / AI-Generated Content Detected',
    forgeryColor: isAuthentic ? '#27ae60' : '#ef4444',
    suspicionReasons: suspicionReasons
  };
  
  if (isAuthentic) {
    results.report = `✓ AUTHENTIC DOCUMENT\n\nThis academic document has passed all verification checks:\n- Digital signature is valid and verified\n- Document integrity is intact with no signs of tampering\n- Metadata is complete and consistent with document content\n- No plagiarism or paraphrasing detected\n- Writing style is consistent indicating single authorship\n- Confidence Level: ${confidence}%\n\nThis document is suitable for official academic and professional use.`;
  } else {
    results.report = `✗ SUSPICIOUS DOCUMENT - FAKE/FORGED DETECTED\n\nThis document has raised serious red flags:\n${suspicionReasons.map(r => `- ${r}`).join('\n')}\n\nAdditional Issues:\n- Plagiarism Score: ${plagiarismScore}% (Content copied from other sources)\n- Paraphrasing Score: ${paraphrasingScore}% (Content rewritten from other sources)\n- Digital Signature: Invalid or Missing\n- Document Integrity: COMPROMISED\n- Forgery Detection: ${Math.random() > 0.5 ? 'AI-Generated Content Detected' : 'Manual Alteration Signatures Found'}\n- Confidence Level: ${confidence}%\n\n⚠️ WARNING: This document appears to be FAKE or FORGED. Do NOT accept this document for official purposes. Contact the issuing institution to verify authenticity.`;
  }
  
  return results;
}

// Download verification report
function downloadReport() {
  const fileName = document.getElementById('resultFileName').textContent;
  const statusBadge = document.getElementById('statusBadge').textContent;
  const confidence = document.getElementById('confidenceScore').textContent;
  const report = document.getElementById('resultReport').textContent;
  
  const reportContent = `
AUTHENTICCHECK - VERIFICATION REPORT
=====================================
Generated: ${new Date().toLocaleString()}

Document Information:
- File Name: ${fileName}
- Document Type: ${document.getElementById('resultFileType').textContent}
- File Size: ${document.getElementById('resultFileSize').textContent}

Verification Status:
${statusBadge}
${confidence}

Analysis Details:
- Digital Signature: ${document.getElementById('resultSignature').textContent}
- Document Integrity: ${document.getElementById('resultIntegrity').textContent}
- Metadata Status: ${document.getElementById('resultMetadata').textContent}
- Forgery Detection: ${document.getElementById('resultForgery').textContent}

Detailed Report:
${report}

=====================================
This is an automated verification report. For official purposes, please consult the issuing institution.
  `;
  
  const blob = new Blob([reportContent], { type: 'text/plain' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `AuthentiCheck_Report_${Date.now()}.txt`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

// Upload another document
function uploadAnother() {
  document.getElementById('uploadForm').reset();
  document.getElementById('resultSection').style.display = 'none';
  document.getElementById('docFile').focus();
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Initialize tooltips or other interactive features
function initializePageFeatures() {
  console.log('AuthentiCheck website loaded successfully');
  // initialize stored docs features if present on the page
  try { initStoredDocsFeatures(); } catch (e) { /* ignore if not present */ }
}

window.addEventListener('load', initializePageFeatures);

// Initialize stored documents UI behaviors (search, refresh auto-update)
function initStoredDocsFeatures() {
  const searchInput = document.getElementById('storedDocsSearch');
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      if (storedSearchDebounce) clearTimeout(storedSearchDebounce);
      storedSearchDebounce = setTimeout(() => {
        searchStoredDocs();
      }, 300);
    });
  }

  // Start auto-refresh only if the stored docs container exists
  const storedContainer = document.getElementById('storedDocsList');
  if (storedContainer) {
    // initial load
    fetchStoredDocuments();
    // start periodic refresh every 30 seconds
    startAutoRefresh(30000);
    // stop auto-refresh when leaving page
    window.addEventListener('beforeunload', () => stopAutoRefresh());
  }
}

// View full verification report
function viewFullReport() {
  window.location.href = '/report';
}

// Upload selected file to backend DB for future referencing
function uploadToDB() {
  // Use the visible file input (docFileForm) for upload
  const fileInput = document.getElementById('docFileForm');
  if (!fileInput || fileInput.files.length === 0) {
    showMiniPopup('Please select a file before uploading to DB');
    return;
  }
  const file = fileInput.files[0];
  const form = new FormData();
  form.append('file', file);
  // Attach suspicious findings if available (from last verification)
  if (window.lastSuspiciousFindings) {
    form.append('suspicious', JSON.stringify(window.lastSuspiciousFindings));
  }
  // Attach uploader ID
  const uploaderId = window.lastUploaderId || localStorage.getItem('authenticheck_user_id') || localStorage.getItem('authenticheck_user_name');
  if (uploaderId) {
    form.append('uploader_id', uploaderId);
  }

  fetch('http://127.0.0.1:5050/api/upload', {
    method: 'POST',
    body: form
  }).then(r => r.json())
    .then(data => {
      if (data && data.status === 'ok') {
        showMiniPopup('File saved to DB (id: ' + data.id + ', sha256: ' + data.sha256 + ')');
      } else {
        showMiniPopup('Upload failed: ' + JSON.stringify(data));
      }
    }).catch(err => {
      showMiniPopup('Upload error: ' + err);
    });
}

// Fetch stored documents from backend and render them in the page
function fetchStoredDocuments() {
  const container = document.getElementById('storedDocsList');
  if (!container) return;
  container.innerHTML = '<p style="color:#64748b;">Loading stored documents...</p>';

  fetch('http://127.0.0.1:5050/api/documents')
    .then(r => r.json())
    .then(docs => {
      storedDocsCache = docs || [];
      renderStoredDocuments(storedDocsCache);
    })
    .catch(err => {
      console.error('Error fetching documents', err);
      container.innerHTML = '<p style="color:#ef4444;">Failed to load documents. Is the backend running?</p>';
    });
}

// Client-side search/filter for stored documents
function searchStoredDocs() {
  const qEl = document.getElementById('storedDocsSearch');
  if (!qEl) return;
  const q = (qEl.value || '').trim().toLowerCase();
  if (!q) {
    renderStoredDocuments(storedDocsCache);
    return;
  }

  const filtered = storedDocsCache.filter(d => {
    const name = (d.filename || '').toLowerCase();
    const sha = (d.sha256 || '').toLowerCase();
    const uploaded = d.upload_time ? new Date(d.upload_time).toLocaleString().toLowerCase() : '';
    const isRef = d.is_reference ? 'reference' : 'stored';
    return name.includes(q) || sha.includes(q) || uploaded.includes(q) || isRef.includes(q);
  });

  renderStoredDocuments(filtered);
}

// Auto-refresh control
function startAutoRefresh(intervalMs) {
  stopAutoRefresh();
  storedAutoRefreshTimer = setInterval(() => {
    fetchStoredDocuments();
  }, intervalMs || 30000);
}

function stopAutoRefresh() {
  if (storedAutoRefreshTimer) {
    clearInterval(storedAutoRefreshTimer);
    storedAutoRefreshTimer = null;
  }
}

function renderStoredDocuments(docs) {
  const container = document.getElementById('storedDocsList');
  if (!container) return;
  // Filter docs for current user
  const userId = localStorage.getItem('authenticheck_user_id') || localStorage.getItem('authenticheck_user_name');
  const userDocs = docs.filter(d => d.uploader_id === userId);
  if (!userDocs || userDocs.length === 0) {
    container.innerHTML = '<p style="margin:0; color:#64748b;">No documents stored yet.</p>';
    return;
  }

  let html = '<table style="width:100%; border-collapse:collapse; font-size:0.95rem;">';
  html += '<thead><tr style="text-align:left; color:#0f172a;"><th>File</th><th>Size</th><th>SHA-256</th><th>Ref</th><th>Uploaded</th></tr></thead>';
  html += '<tbody>';
  docs.forEach(d => {
    const fileLink = `<a href="http://127.0.0.1:5050/uploads/${encodeURIComponent(d.filename)}" target="_blank">${escapeHtml(d.filename)}</a>`;
    const sizeKB = d.size ? Math.round(d.size / 1024) + ' KB' : '-';
    const sha = d.sha256 ? (d.sha256.substring(0, 16) + '...') : '-';
    const isRef = d.is_reference ? '<span style="color:#065f46;font-weight:600;">YES</span>' : 'NO';
    const uploaded = d.upload_time ? new Date(d.upload_time).toLocaleString() : '-';
    html += `<tr style="border-top:1px solid #e6edf3;"><td>${fileLink}</td><td>${sizeKB}</td><td style="font-family:monospace">${sha}</td><td>${isRef}</td><td>${uploaded}</td></tr>`;
  });
  html += '</tbody></table>';
  container.innerHTML = html;
}

function escapeHtml(str) {
  if (str === undefined || str === null) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// Call backend to seed reference files into DB (reference_files folder)
function seedReferencesFrontend() {
  const container = document.getElementById('storedDocsList');
  if (container) container.innerHTML = '<p style="color:#64748b;">Seeding reference documents...</p>';

  fetch('http://127.0.0.1:5050/api/reference/seed', { method: 'POST' })
    .then(r => r.json())
    .then(res => {
      showMiniPopup('Reference seed completed. Added: ' + (res.added || 0));
      fetchStoredDocuments();
    })
    .catch(err => {
      console.error('Seed failed', err);
      if (container) container.innerHTML = '<p style="color:#ef4444;">Seeding failed. Check backend.</p>';
    });
}


// ========== UPLOADED DOCUMENTS FUNCTIONS ==========

// Fetch uploaded documents from backend and render them in the page
function fetchUploadedDocuments() {
  const container = document.getElementById('uploadedDocsList');
  if (!container) return;
  container.innerHTML = '<p style="color:#64748b;">Loading your uploaded documents...</p>';

  fetch('http://127.0.0.1:5050/api/documents/uploaded')
    .then(r => r.json())
    .then(docs => {
      uploadedDocsCache = docs || [];
      renderUploadedDocuments(uploadedDocsCache);
    })
    .catch(err => {
      console.error('Error fetching uploaded documents', err);
      container.innerHTML = '<p style="color:#ef4444;">Failed to load documents. Is the backend running?</p>';
    });
}

// Client-side search/filter for uploaded documents
function searchUploadedDocs() {
  const qEl = document.getElementById('uploadedDocsSearch');
  if (!qEl) return;
  const q = (qEl.value || '').trim().toLowerCase();
  if (!q) {
    renderUploadedDocuments(uploadedDocsCache);
    return;
  }

  const filtered = uploadedDocsCache.filter(d => {
    const name = (d.filename || '').toLowerCase();
    const sha = (d.sha256 || '').toLowerCase();
    const uploaded = d.upload_time ? new Date(d.upload_time).toLocaleString().toLowerCase() : '';
    return name.includes(q) || sha.includes(q) || uploaded.includes(q);
  });

  renderUploadedDocuments(filtered);
}

// Render uploaded documents in a table format
function renderUploadedDocuments(docs) {
  const container = document.getElementById('uploadedDocsList');
  if (!container) return;
  if (!docs || docs.length === 0) {
    container.innerHTML = '<p style="margin:0; color:#64748b;"><i class="fas fa-inbox"></i> No documents uploaded yet. Start by <a href="/upload" style="color:#3b82f6; text-decoration:underline;">uploading a document</a>.</p>';
    return;
  }

  let html = '<table style="width:100%; border-collapse:collapse; font-size:0.95rem;">';
  html += '<thead><tr style="background:#f1f5f9; text-align:left; color:#0f172a; padding:0.8rem; border-bottom:2px solid #cbd5e1;"><th style="padding:0.8rem;">File Name</th><th style="padding:0.8rem;">Size</th><th style="padding:0.8rem;">SHA-256 Hash</th><th style="padding:0.8rem;">Upload Date</th><th style="padding:0.8rem;">Action</th></tr></thead>';
  html += '<tbody>';
  docs.forEach(d => {
    const fileLink = `<a href="http://127.0.0.1:5050/uploads/${encodeURIComponent(d.filename)}" target="_blank" style="color:#3b82f6; text-decoration:none;"><i class="fas fa-file-download"></i> ${escapeHtml(d.filename)}</a>`;
    const sizeKB = d.size ? Math.round(d.size / 1024) + ' KB' : '-';
    const sha = d.sha256 ? (d.sha256.substring(0, 16) + '...') : '-';
    const uploaded = d.upload_time ? new Date(d.upload_time).toLocaleString() : '-';
    let details = `<div style='font-family:Inter,sans-serif;max-width:340px;background:#fff;border-radius:8px;padding:1.2rem 1.5rem;box-shadow:0 2px 12px #0001;'>`;
    details += `<h3 style='margin-top:0;margin-bottom:1rem;font-size:1.2rem;color:#1e293b;'><i class='fas fa-file-alt' style='color:#3b82f6;'></i> Document Report</h3>`;
    details += `<div style='margin-bottom:0.7rem;'><b>File Name:</b> <span style='color:#334155;'>${escapeHtml(d.filename)}</span></div>`;
    details += `<div style='margin-bottom:0.7rem;'><b>Size:</b> <span style='color:#334155;'>${sizeKB}</span></div>`;
    details += `<div style='margin-bottom:0.7rem;'><b>SHA-256:</b> <span style='font-family:monospace;font-size:0.95em;color:#64748b;'>${d.sha256}</span></div>`;
    details += `<div style='margin-bottom:0.7rem;'><b>Upload Date:</b> <span style='color:#334155;'>${uploaded}</span></div>`;
    if (d.suspicious && d.suspicious.length > 0) {
      details += `<div style='margin-bottom:0.7rem;'><b>Suspicious Findings:</b><ul style='margin:0.3em 0 0 1.2em;color:#dc2626;'>`;
      d.suspicious.forEach(item => {
        if (typeof item === 'object') {
          let finding = '';
          if (item.type) finding += `<b>Type:</b> ${escapeHtml(item.type)}<br/>`;
          if (item.issue) finding += `<b>Issue:</b> ${escapeHtml(item.issue)}<br/>`;
          if (item.content) finding += `<b>Content:</b> ${escapeHtml(item.content)}<br/>`;
          if (item.location) finding += `<b>Location:</b> ${escapeHtml(item.location)}<br/>`;
          if (item.percentage !== undefined) finding += `<b>Score:</b> ${escapeHtml(item.percentage)}%<br/>`;
          details += `<li>${finding}</li>`;
        } else {
          details += `<li>${escapeHtml(item)}</li>`;
        }
      });
      details += `</ul></div>`;
    } else {
      // Show authenticity scores if available
      details += `<div style='margin-bottom:0.7rem;'><b>Module Authenticity Scores:</b><ul style='margin:0.3em 0 0 1.2em;color:#059669;'>`;
      if (d.plagiarismScore !== undefined) details += `<li><b>Plagiarism:</b> ${escapeHtml(d.plagiarismScore)}%</li>`;
      if (d.paraphrasingScore !== undefined) details += `<li><b>Paraphrasing:</b> ${escapeHtml(d.paraphrasingScore)}%</li>`;
      if (d.forgeryScore !== undefined) details += `<li><b>Forgery Detection:</b> ${escapeHtml(d.forgeryScore)}%</li>`;
      if (d.authorshipScore !== undefined) details += `<li><b>Authorship Analysis:</b> ${escapeHtml(d.authorshipScore)}%</li>`;
      details += `</ul></div>`;
      details += `<div style='margin-bottom:0.7rem;'><b>Detected Results:</b> <span style='color:#059669;'>No suspicious findings.</span></div>`;
    }
    details += `</div>`;
    html += `<tr style="border-top:1px solid #e6edf3;"><td style="padding:0.8rem;">${fileLink}</td><td style="padding:0.8rem;">${sizeKB}</td><td style="padding:0.8rem; font-family:monospace; font-size:0.85rem;">${sha}</td><td style="padding:0.8rem;">${uploaded}</td><td style="padding:0.8rem;"><button onclick="showUploadedDocDetails('${encodeURIComponent(d.filename)}')" class="btn btn-primary" style="padding:0.4rem 0.8rem; font-size:0.9rem;"><i class="fas fa-eye"></i> View Details</button></td></tr>`;
  // Show details below the table
  function showUploadedDocDetails(filename) {
    const docs = uploadedDocsCache || [];
    const decoded = decodeURIComponent(filename);
    const d = docs.find(doc => doc.filename === decoded);
    if (!d) return;
      // Instead of showing inline, open report.html in the same tab with ?file=filename
      window.location.href = `report.html?file=${encodeURIComponent(d.filename)}`;
  }
  window.showUploadedDocDetails = showUploadedDocDetails;
  });
  html += '</tbody></table>';
  container.innerHTML = html;
}

