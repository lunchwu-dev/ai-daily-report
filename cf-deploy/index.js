export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // 静态HTML内容
    const htmlContent = await env.AI_REPORTS.get("report-2026-03-02") || getDefaultReport();
    
    if (url.pathname === "/" || url.pathname === "/index.html") {
      return new Response(htmlContent, {
        headers: {
          "Content-Type": "text/html; charset=utf-8",
          "Cache-Control": "public, max-age=3600"
        }
      });
    }
    
    if (url.pathname === "/api/summary") {
      const summary = await env.AI_REPORTS.get("summary-2026-03-02");
      return new Response(summary || "{}", {
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Access-Control-Allow-Origin": "*"
        }
      });
    }
    
    return new Response("Not Found", { status: 404 });
  }
};

function getDefaultReport() {
  return `<!DOCTYPE html>
<html>
<head><title>AI日报</title></head>
<body><h1>AI日报 - 2026年03月02日</h1><p>请查看最新报告</p></body>
</html>`;
}
