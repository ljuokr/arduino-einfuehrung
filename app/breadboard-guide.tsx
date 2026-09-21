export function BreadboardGuide() {
  const columns = [146, 174, 202, 230, 258, 342, 370, 398, 426, 454];
  const rows = [90, 126, 162, 198, 234];
  return (
    <figure className="breadboard-guide">
      <div
        className="breadboard-diagram"
        tabIndex={0}
        role="region"
        aria-label="Breadboard-Diagramm, bei Bedarf seitlich verschiebbar"
      >
        <svg
          viewBox="0 0 500 312"
          role="img"
          aria-labelledby="breadboard-title breadboard-description"
        >
          <title id="breadboard-title">
            So sind die Löcher eines Breadboards verbunden
          </title>
          <desc id="breadboard-description">
            Vereinfachter Ausschnitt. Pro nummerierter Reihe sind a bis e
            miteinander verbunden und f bis j miteinander verbunden. Zwischen e
            und f liegt eine trennende Mittelrille. Unterschiedliche Reihen sind
            getrennt. Die beiden links gezeigten Versorgungsschienen verlaufen
            längs und sind voneinander getrennt.
          </desc>
          <rect
            x="14"
            y="46"
            width="470"
            height="220"
            rx="8"
            fill="#fff"
            stroke="#a8aaad"
          />
          <rect x="281" y="48" width="39" height="216" fill="#eef0f1" />
          <g
            fontFamily="Lato, Arial, sans-serif"
            fontSize="18"
            textAnchor="middle"
            fill="#30383a"
          >
            <text x="48" y="35" fill="#9c2424">
              +
            </text>
            <text x="80" y="35" fill="#1b5390">
              −
            </text>
            {columns.map((x, i) => (
              <text key={x} x={x} y="35">
                {'abcdefghij'[i]}
              </text>
            ))}
            {rows.map((y, i) => (
              <text key={y} x="116" y={y + 6}>
                {i + 1}
              </text>
            ))}
          </g>
          <path d="M48 74V249" stroke="#a72f2f" strokeWidth="5" />
          <path d="M80 74V249" stroke="#245b98" strokeWidth="5" />
          {rows.map((y) => (
            <g key={y}>
              <path
                d={`M146 ${y}H258 M342 ${y}H454`}
                stroke={y === 126 ? '#28735a' : '#acb7b3'}
                strokeWidth="8"
                strokeLinecap="round"
              />
              {[48, 80, ...columns].map((x) => (
                <circle
                  key={x}
                  cx={x}
                  cy={y}
                  r="5"
                  fill="#fff"
                  stroke="#495253"
                  strokeWidth="2"
                />
              ))}
            </g>
          ))}
          <path d="M300 275V290" stroke="#647074" />
          <text
            x="300"
            y="307"
            fontFamily="Lato, Arial, sans-serif"
            fontSize="18"
            textAnchor="middle"
            fill="#30383a"
          >
            Mittelrille: keine Verbindung
          </text>
        </svg>
      </div>
      <figcaption>
        Vereinfachter Ausschnitt: Die Linien zeigen die Kontakte im Innern. Die
        seitlichen Schienen können je nach Breadboard unterbrochen sein.
      </figcaption>
    </figure>
  );
}
