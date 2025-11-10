<style>
    /* Estilos específicos para esta página para não quebrar o resto do seu app */
    #job-families-view {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #334155; /* Slate-700 */
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
    }

    #job-families-view h1.page-title {
        font-size: 1.8rem;
        color: #0f172a; /* Slate-900 */
        margin-bottom: 0.5rem;
    }

    #job-families-view .page-subtitle {
        color: #64748b; /* Slate-500 */
        margin-bottom: 2rem;
    }

    /* Container do Seletor */
    .jf-selector-box {
        background: #f8fafc;
        border: 2px dashed #cbd5e1;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    .jf-selector-box select {
        padding: 10px 15px;
        font-size: 1rem;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        width: 100%;
        max-width: 400px;
        cursor: pointer;
    }

    /* Cartão de Conteúdo */
    .jf-card {
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        overflow: hidden;
        display: none; /* Inicialmente oculto */
        animation: slideUp 0.4s ease-out;
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .jf-card-header {
        background: #2563eb; /* Ajuste para a cor primária do seu app se desejar */
        color: white;
        padding: 1.5rem 2rem;
    }

    .jf-card-header h2 {
        margin: 0;
        font-size: 1.5rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .jf-motto {
        opacity: 0.9;
        font-style: italic;
        margin-top: 8px;
        font-weight: 300;
    }

    .jf-card-body {
        padding: 2rem;
    }

    .jf-section {
        margin-bottom: 2rem;
    }

    .jf-section h3 {
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #2563eb;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    .jf-section ul {
        padding-left: 1.5rem;
    }
    .jf-section li {
        margin-bottom: 0.5rem;
    }

    .jf-empty-state {
        text-align: center;
        padding: 3rem;
        color: #94a3b8;
    }

</style>

<div id="job-families-view">
    <div>
        <h1 class="page-title">Conheça Nossas Job Families</h1>
        <p class="page-subtitle">
            Explore as áreas de especialização da empresa. Selecione uma família abaixo para ver seus detalhes, missão e escopo de atuação.
        </p>
    </div>

    <div class="jf-selector-box">
        <label for="jf-selector" style="display: block; margin-bottom: 15px; font-weight: 600; color: #475569;">
            Qual área você quer explorar hoje?
        </label>
        <select id="jf-selector">
            <option value="">-- Selecione uma família --</option>
            </select>
    </div>

    <div id="jf-empty" class="jf-empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 1rem; opacity: 0.5;">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <p>Aguardando seleção...</p>
    </div>

    <div id="jf-content-card" class="jf-card">
        <div class="jf-card-header">
            <h2 id="jf-title"></h2>
            <div id="jf-motto" class="jf-motto"></div>
        </div>
        <div class="jf-card-body">
            <div class="jf-section">
                <h3>🎯 Nossa Missão</h3>
                <p id="jf-mission"></p>
            </div>

            <div class="jf-section" style="display: flex; gap: 2rem; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 250px;">
                    <h3>🛠️ O que fazemos</h3>
                    <ul id="jf-activities">
                        </ul>
                </div>
                <div style="flex: 1; min-width: 250px; background: #f8fafc; padding: 1.5rem; border-radius: 8px;">
                    <h3 style="border: none; margin-bottom: 10px;">👥 Quem somos</h3>
                    <p id="jf-profile" style="font-size: 0.95rem;"></p>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    // =================================================================
    // DADOS (Substitua pelos dados reais do seu Excel)
    // =================================================================
    const jfData = {
        "tech": {
            title: "Tecnologia & Engenharia",
            icon: "💻",
            motto: "Construindo o motor digital da nossa inovação.",
            mission: "Responsável por desenhar, desenvolver e manter nossos produtos digitais, garantindo escalabilidade, segurança e alta performance.",
            activities: ["Desenvolvimento Frontend/Backend", "DevOps & Infraestrutura Cloud", "QA e Testes Automatizados", "Arquitetura de Software"],
            profile: "Profissionais com forte raciocínio lógico, apaixonados por código e resolução de problemas complexos."
        },
        "sales": {
            title: "Vendas (Sales)",
            icon: "🚀",
            motto: "Conectando nossas soluções a quem precisa delas.",
            mission: "Expandir nossa base de clientes e gerar receita sustentável através de relacionamentos consultivos e estratégicos.",
            activities: ["Prospecção de novos clientes (Hunters)", "Gestão de carteira (Farmers)", "Negociação de contratos", "Demonstrações de produto"],
            profile: "Comunicadores natos, resilientes, orientados a metas e com alta capacidade de persuasão."
        },
        "ops": {
            title: "Operações",
            icon: "⚙️",
            motto: "A excelência invisível que faz tudo funcionar.",
            mission: "Garantir que nossos processos internos e entregas ao cliente ocorram sem atrito, com máxima eficiência e qualidade.",
            activities: ["Suporte ao Cliente N1/N2", "Gestão de Processos", "Onboarding de Clientes", "Logística Interna"],
            profile: "Organizados, ágeis na resolução de crises e obcecados por eficiência."
        }
        // Adicione as outras famílias aqui...
    };

    // =================================================================
    // LÓGICA DE INICIALIZAÇÃO
    // =================================================================
    (function initJobFamilies() {
        const selector = document.getElementById('jf-selector');
        const emptyState = document.getElementById('jf-empty');
        const card = document.getElementById('jf-content-card');

        // Povoar o seletor
        Object.keys(jfData).forEach(key => {
            const opt = document.createElement('option');
            opt.value = key;
            opt.textContent = `${jfData[key].icon} ${jfData[key].title}`;
            selector.appendChild(opt);
        });

        // Evento de mudança
        selector.addEventListener('change', (e) => {
            const key = e.target.value;
            if (!key) {
                card.style.display = 'none';
                emptyState.style.display = 'block';
                return;
            }

            const data = jfData[key];
            
            // Preencher dados
            document.getElementById('jf-title').innerHTML = `${data.icon} ${data.title}`;
            document.getElementById('jf-motto').textContent = `"${data.motto}"`;
            document.getElementById('jf-mission').textContent = data.mission;
            document.getElementById('jf-profile').textContent = data.profile;
            
            const actList = document.getElementById('jf-activities');
            actList.innerHTML = '';
            data.activities.forEach(act => {
                const li = document.createElement('li');
                li.textContent = act;
                actList.appendChild(li);
            });

            // Alternar visualização
            emptyState.style.display = 'none';
            card.style.display = 'block';
        });
    })();
</script>
