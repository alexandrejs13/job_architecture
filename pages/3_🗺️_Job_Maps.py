:root {
  --blue: #145efc;
  --gray-line: #dadada;
  --gray-bg: #f8f9fa;
  --dark-gray: #333333;
}

.block-container {
  max-width: 100% !important;
  margin: 0 !important;
  padding: 1rem 2rem !important;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 200;
  background: white;
  padding: 10px 0 5px 0;
  border-bottom: 2px solid var(--blue);
  margin-bottom: 15px;
}
h1 {
  color: var(--blue);
  font-weight: 900 !important;
  font-size: 1.9rem !important;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px !important;
}

.map-wrapper {
  height: 78vh;
  overflow: auto;
  border-top: 3px solid var(--blue);
  border-bottom: 3px solid var(--blue);
  background: white;
  position: relative;
  will-change: transform;
  box-shadow: 0 0 15px rgba(0,0,0,0.05);
}

.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  width: max-content;
  font-size: 0.88rem;
  grid-auto-rows: minmax(90px, auto);
  row-gap: 0px !important;
  column-gap: 0px !important;
  background-color: var(--gray-line);
}

.jobmap-grid > div {
  background-color: white;
  border-right: 1px solid var(--gray-line);
  border-bottom: 1px solid var(--gray-line);
  box-sizing: border-box;
}

/* Removidas bordas inferiores para eliminar linha cinza entre linha 1 e 2 */
.header-family {
  font-weight: 800;
  color: #fff;
  padding: 10px 5px;
  text-align: center;
  border-right: 1px solid rgba(255,255,255,0.5) !important;
  border-bottom: 0 none !important; /* ALTERAÇÃO AQUI */
  margin-bottom: 0px !important;
  padding-bottom: 10px !important;
  position: sticky;
  top: 0;
  z-index: 56;
  white-space: normal;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-row: 1;
  font-size: 0.9rem;
}

.header-subfamily {
  font-weight: 600;
  color: #333;
  padding: 8px 5px;
  text-align: center;
  position: sticky;
  top: 50px;
  z-index: 55;
  white-space: normal;
  border-top: 0 none !important;
  margin-top: 0px !important;
  border-bottom: 2px solid var(--gray-line) !important;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-row: 2;
  font-size: 0.85rem;
}

.gg-header {
  background: #000 !important;
  color: white;
  font-weight: 800;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-row: 1 / span 2;
  grid-column: 1;
  position: sticky;
  left: 0;
  top: 0;
  z-index: 60;
  border-right: 2px solid white !important;
  border-bottom: none !important;  /* ALTERAÇÃO AQUI */
}

.gg-cell {
  background: #000 !important;
  color: white;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  position: sticky;
  left: 0;
  z-index: 55;
  border-right: 2px solid white !important;
  border-top: 1px solid white !important;
  grid-column: 1;
  font-size: 0.9rem;
}

.cell {
  background: white !important;
  padding: 8px;
  text-align: left;
  vertical-align: middle;
  z-index: 1;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  align-content: center;
}

.job-card {
  background: #f9f9f9;
  border-left: 4px solid var(--blue);
  border-radius: 6px;
  padding: 6px 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  font-size: 0.75rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  width: 135px;
  height: 75px;
  flex: 0 0 135px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}
.job-card b {
  display: block;
  font-weight: 700;
  margin-bottom: 3px;
  line-height: 1.15;
  color: #222;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.job-card span {
  display: block;
  font-size: 0.7rem;
  color: #666;
  line-height: 1.1;
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gg-header::after, .gg-cell::after {
  content: "";
  position: absolute;
  right: -5px;
  top: 0;
  bottom: 0;
  width: 5px;
  background: linear-gradient(to right, rgba(0,0,0,0.15), transparent);
  pointer-events: none;
}

@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
