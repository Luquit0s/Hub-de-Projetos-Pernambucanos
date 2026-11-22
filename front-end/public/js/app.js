// Ajuste se o Django rodar em outra porta
const API_URL = 'http://localhost:8000';
// Chave onde o login (feito por outra pessoa) guarda o JWT
const TOKEN_KEY = 'access';
const LOGIN_PAGE = '/login.html';

const esc = (s = '') => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function irParaLogin() {
  window.location.href = LOGIN_PAGE;
  return new Promise(() => {});
}

async function api(path, opts = {}) {
  const token = localStorage.getItem(TOKEN_KEY);
  if (!token) return irParaLogin();
  const res = await fetch(API_URL + path, {
    ...opts,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}`, ...opts.headers },
  });
  if (res.status === 401) return irParaLogin();
  if (!res.ok) throw new Error(`Erro ${res.status}`);
  return res.status === 204 ? null : res.json();
}

async function listarProjetos() {
  const dados = await api('/api/projetos/');
  return Array.isArray(dados) ? dados : dados.results || [];
}

function nomeDe(u) {
  return [u.first_name, u.last_name].filter(Boolean).join(' ') || u.username;
}

const iniciais = n => n.split(' ').slice(0, 2).map(p => p[0]).join('').toUpperCase();

const ICONE_CFG = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>';

// Monta a barra lateral e devolve o usuário logado
async function montarSidebar(ativo) {
  const me = await api('/api/auth/me/');
  const nome = nomeDe(me);
  const link = (id, href, txt) => `<a href="${href}" class="${ativo === id ? 'on' : ''}" ${ativo === id ? 'aria-current="page"' : ''}>${txt}</a>`;
  document.getElementById('side').innerHTML = `
    <div class="avatar" aria-hidden="true">${esc(iniciais(nome))}</div>
    <div class="nome">${esc(nome)}</div>
    <nav>${link('projetos', '/projetos.html', 'Projetos')}${link('perfil', '/perfil.html', 'Perfil')}${link('contatos', '/contatos.html', 'Contatos')}</nav>
    <a class="cfg" href="#" aria-label="Configurações">${ICONE_CFG}</a>`;
  return me;
}

// Capa: sem campo de imagem na API, usa bloco azul com a inicial
const capaHtml = p => `<div class="capa" aria-hidden="true">${esc((p.titulo || '?')[0].toUpperCase())}</div>`;
