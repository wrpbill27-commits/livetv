// PUTV Stream Proxy Worker
// ป้องกัน hotlinking + rate limiting
// Deploy to Cloudflare Workers

const PUTV_TOKEN = 'staod9t4hsgr';
const ALLOWED_REFERRERS = [
  'wrpbill27-commits.github.io',
  'localhost',
  '127.0.0.1'
];

// Rate limit: 30 req/min per IP
const RATE_LIMIT = new Map();

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const referer = request.headers.get('Referer') || '';
    
    // Get channel code and resolution
    const code = url.searchParams.get('code');
    const res = url.searchParams.get('res') || '720';
    
    if (!code) {
      return new Response('Missing channel code (?code=xxx)', { status: 400 });
    }
    
    // Rate limit check
    const now = Date.now();
    const ipKey = `${ip}_${Math.floor(now / 60000)}`; // reset every minute
    const count = (RATE_LIMIT.get(ipKey) || 0) + 1;
    RATE_LIMIT.set(ipKey, count);
    
    if (count > 30) {
      return new Response('Rate limited. Try again later.', { status: 429 });
    }
    
    // Clean up old rate limit entries
    if (RATE_LIMIT.size > 10000) {
      const cutoff = now - 120000;
      for (const [key] of RATE_LIMIT) {
        const ts = parseInt(key.split('_')[1]) * 60000;
        if (ts < cutoff) RATE_LIMIT.delete(key);
      }
    }
    
    // Referrer check
    const isAllowed = ALLOWED_REFERRERS.some(r => referer.includes(r));
    
    if (!isAllowed) {
      // Block hotlinking - redirect to our site
      return Response.redirect('https://wrpbill27-commits.github.io/livetv/', 302);
    }
    
    // Build stream URL
    const streamUrl = `https://lovetv.workers.dev/lx-${PUTV_TOKEN}/${code}_${res}/playlist.m3u8`;
    
    // Redirect to actual stream
    return Response.redirect(streamUrl, 302);
  }
};
