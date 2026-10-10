(() => {
  document.querySelectorAll('img[data-ml-fallback]').forEach(img => {
    const fallback = () => {
      const src = img.dataset.mlFallback;
      if (!src) return;
      delete img.dataset.mlFallback;
      img.removeAttribute('srcset');
      img.src = src;
    };
    img.addEventListener('error', fallback, {once:true});
    if (img.complete && !img.naturalWidth) fallback();
  });
  document.addEventListener('click', event => {
    const link = event.target.closest?.('.ml-network-nav a,.ml-network-cta a,.ml-network-dock a');
    if (link && typeof window.gtag === 'function') {
      window.gtag('event','brand_cta_click',{brand:'MuscleLove',placement:'network',link_url:link.href});
    }
  });
})();
