export function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-200 mt-auto">
      <div className="container py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h6 className="font-semibold mb-3">О сайте</h6>
            <p className="text-sm text-slate-400">
              ✿Hokkaido Tours✿ — ваш надежный партнер в организации туров по Хоккайдо.
              Бро, ты умрешь и тд. от удовольствия, когда посетишь эти места с нами!
            </p>
          </div>
          <div>
            <h6 className="font-semibold mb-3">Мы в соцсетях</h6>
            <ul className="text-sm space-y-2">
              <li>
                <a href="http://t.me/cahek_aka_zzisst" className="text-slate-400 hover:text-white transition-colors">
                  Messenger MAX
                </a>
              </li>
              <li>
                <a href="https://vk.com/zzisst" className="text-slate-400 hover:text-white transition-colors">
                  VKontakte
                </a>
              </li>
              <li>
                <a href="https://my.itmo.ru/persons/413075" className="text-slate-400 hover:text-white transition-colors">
                  my.itmo
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="border-t border-slate-700 mt-6 pt-6 text-center text-sm text-slate-400">
          <p>
            © 2023-2026 ZZISST, Inc. | All rights reserved |{' '}
            <a href="/terms" className="hover:text-white transition-colors">
              Terms & Conditions
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
}
