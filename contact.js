/* MJB contact: validate, then send the request to the owner's email through FormSubmit.
   If sending fails, the visitor gets a ready message to send from their own email app or to copy.
   WhatsApp buttons show only when a number is set below. */
(() => {
  'use strict';
  const form = document.getElementById('req');
  if (!form) return;
  const OWNER = 'mohammadbakerwork@gmail.com';
  const ENDPOINT = 'https://formsubmit.co/ajax/' + OWNER;
  // WhatsApp number in international format, digits only (for example 9665XXXXXXXX). Leave empty to hide the WhatsApp buttons.
  const WA = '';

  const arabic = () => document.documentElement.lang === 'ar';
  const text = (en, ar) => arabic() ? ar : en;
  const value = key => form.elements[key].value.trim();
  const done = document.getElementById('reqDone');
  const note = document.getElementById('reqMsg');
  const preview = document.getElementById('reqPreview');
  const previewBox = preview.closest('label');
  const acts = done.querySelector('.acts');
  const open = document.getElementById('reqOpen');
  const copy = document.getElementById('reqCopy');
  const btn = document.getElementById('reqBtn');
  const btnLabel = btn.innerHTML;
  const waTop = document.getElementById('waBtn');
  const waDone = document.getElementById('reqWa');
  const waLink = message => `https://wa.me/${WA}?text=${encodeURIComponent(message)}`;
  let state = 'idle'; // idle | sending | sent | fallback
  let snap = null;    // the request as it was sent, in both languages (fields are cleared after a successful send)

  const digits = v => v.replace(/[٠-٩]/g, d => '٠١٢٣٤٥٦٧٨٩'.indexOf(d)).replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d));
  const phone = v => digits(v).replace(/[\s\-().]/g, '');
  const mark = (key, valid, message) => {
    const input = form.elements[key];
    const label = input.closest('label');
    let error = label.querySelector('.err');
    label.classList.toggle('bad', !valid);
    if (!valid) {
      if (!error) {
        error = document.createElement('small');
        error.className = 'err';
        error.id = `req-error-${key}`;
        label.append(error);
      }
      error.textContent = message;
      input.setAttribute('aria-invalid', 'true');
      input.setAttribute('aria-describedby', error.id);
    } else {
      if (error) error.remove();
      input.removeAttribute('aria-invalid');
      input.removeAttribute('aria-describedby');
    }
    return valid;
  };
  const validate = () => {
    const results = [];
    results.push(mark('name', value('name').length > 1, text('Please add your name.', 'اكتب اسمك من فضلك.')));
    const email = value('email');
    const mobile = phone(value('phone'));
    const hasContact = !!(email || mobile);
    results.push(mark('email', hasContact && (!email || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)),
      hasContact ? text('Check this email address.', 'تحقّق من البريد الإلكتروني.') : text('Add your email or mobile number.', 'أضف بريدك أو رقم جوالك.')));
    results.push(mark('phone', !mobile || /^(?:\+?9665\d{8}|009665\d{8}|05\d{8}|\+?[1-9]\d{7,14})$/.test(mobile), text('Check this mobile number.', 'تحقّق من رقم الجوال.')));
    results.push(mark('service', !!value('service'), text('Choose a service.', 'اختر الخدمة.')));
    const low = digits(value('bmin'));
    const high = digits(value('bmax'));
    const validLow = !form.elements.bmin.validity.badInput && (!low || (Number.isFinite(Number(low)) && Number(low) >= 0));
    const validHigh = !form.elements.bmax.validity.badInput && (!high || (Number.isFinite(Number(high)) && Number(high) >= 0));
    results.push(mark('bmin', validLow, text('Enter a budget of zero or more.', 'اكتب ميزانية صفر أو أكثر.')));
    results.push(mark('bmax', validHigh && !(low && high && Number(low) > Number(high)), text('The upper budget must be zero or more and at least the lower budget.', 'الحد الأعلى لا يكون سالبًا أو أقل من الحد الأدنى.')));
    results.push(mark('details', value('details').length >= 20, text('Add at least 20 characters about your idea.', 'اكتب تفاصيل عن فكرتك: 20 حرفًا على الأقل.')));
    return results.every(Boolean);
  };

  // the request, in the visitor's language for the preview and in both languages for the email
  const budgetOf = ar => {
    const low = digits(value('bmin'));
    const high = digits(value('bmax'));
    const f = n => Number(n).toLocaleString('en-US');
    if (low && high) return `${f(low)}–${f(high)} ${ar ? 'ريال' : 'SAR'}`;
    if (low) return ar ? `من ${f(low)} ريال` : `from ${f(low)} SAR`;
    if (high) return ar ? `حتى ${f(high)} ريال` : `up to ${f(high)} SAR`;
    return ar ? 'غير محددة' : 'Not set';
  };
  const pick = (key, ar) => { const o = form.elements[key].selectedOptions[0]; return ar ? o.dataset.ar : o.dataset.en; };
  const message = (ar = arabic()) => (ar
    ? ['طلب مشروع جديد · MJB', `الاسم: ${value('name')}`, `الجوال: ${phone(value('phone')) || '-'}`, `البريد: ${value('email') || '-'}`, `الخدمة: ${pick('service', true)}`, `الميزانية: ${budgetOf(true)}`, `المدة: ${pick('when', true)}`, '', value('details')]
    : ['New project request · MJB', `Name: ${value('name')}`, `Mobile: ${phone(value('phone')) || '-'}`, `Email: ${value('email') || '-'}`, `Service: ${pick('service', false)}`, `Budget: ${budgetOf(false)}`, `Timeline: ${pick('when', false)}`, '', value('details')]
  ).join('\n');

  const setWa = () => {
    const on = !!WA;
    waTop.hidden = !on;
    if (on) waTop.href = waLink(text('Hello Mohammad, I would like to ask about a project.', 'مرحبًا محمد، أبغى أستفسر عن مشروع.'));
    waDone.hidden = !on || state === 'idle';
    if (on && state !== 'idle') {
      waDone.href = waLink(snap ? snap[arabic() ? 'ar' : 'en'] : message());
      waDone.textContent = text('Send on WhatsApp too', 'أرسله على واتساب أيضًا');
    }
  };
  const paint = () => {
    btn.disabled = state === 'sending';
    btn.setAttribute('aria-busy', state === 'sending' ? 'true' : 'false');
    if (state === 'sending') btn.textContent = text('Sending…', 'جارٍ الإرسال…');
    else btn.innerHTML = btnLabel;
    done.hidden = state === 'idle' || state === 'sending';
    const fallback = state === 'fallback';
    previewBox.hidden = !fallback;
    open.hidden = !fallback;
    copy.hidden = !fallback;
    if (state === 'sent') {
      note.textContent = text('Thank you, your request has reached me. I usually reply within two days.', 'شكرًا، وصلني طلبك. أرد عادةً خلال يومين.');
    } else if (fallback) {
      const msg = message();
      preview.value = msg;
      preview.setAttribute('aria-label', text('Prepared message preview', 'معاينة الرسالة الجاهزة'));
      open.href = `mailto:${OWNER}?subject=${encodeURIComponent(text('Project request: ', 'طلب مشروع: ') + pick('service', arabic()))}&body=${encodeURIComponent(msg)}`;
      open.textContent = text('Open email to send', 'افتح البريد للإرسال');
      copy.textContent = text('Copy message', 'انسخ الرسالة');
      note.textContent = text('Your request could not be sent right now. Open your email app to send it, or copy it.', 'تعذّر إرسال طلبك الآن. افتح تطبيق البريد لإرساله، أو انسخ الرسالة.');
    }
    acts.hidden = !(fallback || (WA && state === 'sent'));
    setWa();
  };

  const send = async () => {
    const ctrl = 'AbortController' in window ? new AbortController() : null;
    const timer = ctrl ? setTimeout(() => ctrl.abort(), 15000) : 0;
    try {
      const email = value('email');
      const body = {
        name: value('name'),
        email: email || '-',
        mobile: phone(value('phone')) || '-',
        service: `${pick('service', false)} · ${pick('service', true)}`,
        budget: budgetOf(true),
        timeline: pick('when', true),
        details: value('details'),
        language: arabic() ? 'العربية' : 'English',
        _subject: `طلب مشروع جديد · MJB — ${pick('service', true)}`,
        _template: 'table',
        _captcha: 'false'
      };
      if (email) body._replyto = email;
      const res = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(body),
        signal: ctrl ? ctrl.signal : undefined
      });
      const data = await res.json().catch(() => ({}));
      return res.ok && (data.success === true || data.success === 'true');
    } catch (_) {
      return false;
    } finally {
      clearTimeout(timer);
    }
  };

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (state === 'sending') return;
    if (form.elements.website.value) return;
    if (!validate()) {
      form.querySelector('[aria-invalid="true"]').focus();
      return;
    }
    snap = { ar: message(true), en: message(false) };
    state = 'sending';
    paint();
    state = (await send()) ? 'sent' : 'fallback';
    paint();
    note.setAttribute('tabindex', '-1');
    if (state === 'sent') {
      form.reset();
      note.focus({ preventScroll: true });
    } else {
      preview.focus({ preventScroll: true });
    }
  });
  ['name', 'email', 'phone', 'service', 'bmin', 'bmax', 'when', 'details'].forEach(key => {
    form.elements[key].addEventListener('input', () => {
      if (form.querySelector('.bad')) validate();
      if (state === 'fallback' || state === 'sent') { state = 'idle'; snap = null; paint(); }
    });
  });
  copy.addEventListener('click', async () => {
    try {
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(preview.value);
      copy.textContent = text('Copied', 'تم النسخ');
    } catch (_) {
      preview.focus();
      preview.select();
      copy.textContent = text('Select and copy the message', 'حدّد الرسالة وانسخها');
    }
  });
  document.addEventListener('langchange', () => {
    if (form.querySelector('.bad')) validate();
    paint();
  });
  paint();
})();
