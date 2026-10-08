/* MJB contact: prepare a reviewable email locally; sending remains the visitor's action. */
(() => {
  'use strict';
  const form = document.getElementById('req');
  if (!form) return;
  const owner = 'mohammadbakerwork@gmail.com';
  const arabic = () => document.documentElement.lang === 'ar';
  const text = (en, ar) => arabic() ? ar : en;
  const value = key => form.elements[key].value.trim();
  const done = document.getElementById('reqDone');
  const note = document.getElementById('reqMsg');
  const preview = document.getElementById('reqPreview');
  const open = document.getElementById('reqOpen');
  const copy = document.getElementById('reqCopy');
  let prepared = false;
  const digits = value => value.replace(/[٠-٩]/g, d => '٠١٢٣٤٥٦٧٨٩'.indexOf(d)).replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d));
  const phone = value => digits(value).replace(/[\s\-().]/g, '');
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
  const refresh = () => {
    const service = form.elements.service.selectedOptions[0];
    const timeline = form.elements.when.selectedOptions[0];
    const low = digits(value('bmin'));
    const high = digits(value('bmax'));
    const format = amount => Number(amount).toLocaleString('en-US');
    const budget = low && high ? `${format(low)}–${format(high)} ${text('SAR', 'ريال')}` : low ? text(`from ${format(low)} SAR`, `من ${format(low)} ريال`) : high ? text(`up to ${format(high)} SAR`, `حتى ${format(high)} ريال`) : text('Not set', 'غير محددة');
    const serviceName = arabic() ? service.dataset.ar : service.dataset.en;
    const when = arabic() ? timeline.dataset.ar : timeline.dataset.en;
    const lines = arabic()
      ? ['طلب مشروع جديد · MJB', `الاسم: ${value('name')}`, `الجوال: ${phone(value('phone')) || '-'}`, `البريد: ${value('email') || '-'}`, `الخدمة: ${serviceName}`, `الميزانية: ${budget}`, `المدة: ${when}`, '', value('details')]
      : ['New project request · MJB', `Name: ${value('name')}`, `Mobile: ${phone(value('phone')) || '-'}`, `Email: ${value('email') || '-'}`, `Service: ${serviceName}`, `Budget: ${budget}`, `Timeline: ${when}`, '', value('details')];
    const message = lines.join('\n');
    preview.value = message;
    preview.setAttribute('aria-label', text('Prepared message preview', 'معاينة الرسالة الجاهزة'));
    open.href = `mailto:${owner}?subject=${encodeURIComponent(text('Project request: ', 'طلب مشروع: ') + serviceName)}&body=${encodeURIComponent(message)}`;
    open.textContent = text('Open email to send', 'افتح البريد للإرسال');
    copy.textContent = text('Copy message', 'انسخ الرسالة');
    note.textContent = text('Your message is ready to review. It has not been sent. Open your email app to send it, or copy it.', 'رسالتك جاهزة للمراجعة ولم تُرسل بعد. افتح تطبيق البريد لإرسالها، أو انسخها.');
  };
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (form.elements.website.value) return;
    if (!validate()) {
      form.querySelector('[aria-invalid="true"]').focus();
      return;
    }
    prepared = true;
    done.hidden = false;
    refresh();
    preview.focus({ preventScroll: true });
  });
  ['name', 'email', 'phone', 'service', 'bmin', 'bmax', 'when', 'details'].forEach(key => {
    form.elements[key].addEventListener('input', () => {
      if (form.querySelector('.bad')) validate();
      if (prepared) {
        done.hidden = true;
        prepared = false;
      }
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
    if (prepared) refresh();
  });
})();
