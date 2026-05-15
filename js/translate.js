function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'en,te',
        autoDisplay: false
    }, 'google_translate_element');
}

function toggleLanguage() {
    var btn = document.getElementById('langToggleBtn');
    var select = document.querySelector('.goog-te-combo');
    if (!select) return;
    if (select.value === 'te') {
        select.value = 'en';
        select.dispatchEvent(new Event('change'));
        if (btn) btn.textContent = 'TE';
    } else {
        select.value = 'te';
        select.dispatchEvent(new Event('change'));
        if (btn) btn.textContent = 'EN';
    }
}

// Sync button label on load in case translate cookie is set
document.addEventListener('DOMContentLoaded', function () {
    var waitForSelect = setInterval(function () {
        var select = document.querySelector('.goog-te-combo');
        var btn = document.getElementById('langToggleBtn');
        if (select && btn) {
            clearInterval(waitForSelect);
            btn.textContent = select.value === 'te' ? 'EN' : 'TE';
        }
    }, 300);
});

