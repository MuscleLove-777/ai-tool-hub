// Track the existing brand links through the site's existing analytics instance.
document.addEventListener('click', (event) => {
  const link = event.target.closest('a');
  if (!link || !link.closest('.ml-actions, .ml-always, .promo-musclelove')) return;
  if (typeof window.gtag === 'function') {
    window.gtag('event', 'brand_cta_click', {
      brand: 'MuscleLove',
      placement: link.closest('.ml-always') ? 'persistent' : link.closest('.ml-actions') ? 'hero' : 'footer',
      link_url: link.href
    });
  }
});
