function pivotTable(data, valueColumn, groupColumns, pivotColumns, aggregator = x=>x.length ? x[0] : "") {
    // Helper function
    function span(...args) {
        return [" rowspan", " colspan"].map((dim, i) =>
            args[i] > 1 ? dim + '="' + args[i] + '"' : ""
        ).join``;
    }

    // Structure dimensions:
    const [groups, pivots] = [groupColumns, pivotColumns].map(columns => {
        const colMap = {};
        for (const row of data) {
            columns.reduce((acc, colNo) => (acc[row[colNo]] = acc[row[colNo]] || {}), colMap);
        }
        const headers = columns.map(col => []);
        const tree = (function process(colMap, y=0, x=0) {
            return Object.entries(colMap).reduce((acc, [title, obj]) => {
                const result = process(obj, y+1, x);
                const size = result.size || 1;
                result.title = title;
                acc.children[title] = result;
                acc.size += size;
                headers[y].push(result);
                x += size;
                return acc;
            }, { title: null, x, size: 0, children: {} });
        })(colMap);
        tree.headers = headers;
        return tree;
    });

    // Collect data in matrix, per dimensions:
    const matrix = Array.from({length:groups.size}, row => Array.from({length:pivots.size}, cell => []));
    for (const row of data) {
        const y = groupColumns.reduce((acc, colNo) => acc.children[row[colNo]], groups).x;
        const x = pivotColumns.reduce((acc, colNo) => acc.children[row[colNo]], pivots).x;
        matrix[y][x].push(row[valueColumn]);
    }
    matrix.forEach(row => row.forEach((values,i) => row[i] = aggregator(values)));

    // Produce HTML for column headers:
    let html = `<tr class="header"><th${span(pivotColumns.length, groupColumns.length)}></th>${
        pivots.headers.map(header => header.map(o => `<th${span(1, o.size)} class="text-center">${o.title}</th>`).join``).join("</tr>\n<tr>")
    }</tr>`;

    // Produce HTML for the row headers and cells:
    let startRow = true;
    let y = 0;
    (function loop(children, depth=0) {
        Object.values(children).map(group => {
            if (startRow) html += "<tr>";
            startRow = false;
            html += `<th${span(group.size, 1)}>${group.title}</th>`;
            loop(group.children, depth+1);
        });
        if (depth >= groupColumns.length) {
            html += `${matrix[y].map(value => `<td class="text-center">${value}</td>`).join``}</tr>\n`;
            startRow = true;
            y++;
        }
    })(groups.children);

    return html;
}

function convertCSV(datapoints, indYear, iniYear) {
    const meta = datapoints.metainfo;
    const jerarquias = datapoints.hierarchies;
    const medidas = datapoints.measures;
    const data = datapoints.data;

    const num_j = jerarquias.length;
    const num_m = medidas.length;
    const num_d = data.length;

    let csv = "";
    for (let j = 0; j < num_j; j++)  {
        csv += jerarquias[j].des + "|";
    }
    csv += "medida|valor\n"

    let linea = "";
    for (let d = 0; d < num_d; d++) {
        if (Number(data[d][indYear].des) >= iniYear) {
            for (let m = 0; m < num_m; m++) {
                for (let j = 0; j < num_j; j++) {
                    linea += data[d][j].des + "|";
                }
                linea += medidas[m].des + "|";
		if (data[d][num_j+m].format == undefined) {
		    valor = (Number(data[d][num_j+m].val)).toLocaleString(
			'de-DE',
			{minimumFractionDigits: 2,
			 maximumFractionDigits: 2});
		} else {
		    valor = data[d][num_j+m].format;
		}
                linea += valor + "\n";
            }
            csv += linea;
            linea = "";
        }
    }

    let datos = csv.split("\n").map(function (line) {
        line = line.replace(/^\s*\n?$/gm, "");
        return line.split("|");
    });
    if (datos.pop().length == 0) {
        datos.pop();
    }

    return datos;
}

function twoDecimals(num) {
  return Number(num).toFixed(2);
}

function selector (data,territorio,indice,reverse=0) {
    let datos = data.filter((value) => value[indTerritorio].des == territorio && value[indYear].des >= yearIni).map((value) => value[indice].val);

    let serie = datos.map((x) => Number(x) || null );
    if (reverse == 1) {
	serie = serie.reverse();
    }

    return serie;
}

function seleccion (data,territorio,extra,indice,reverse=0) {
  let serie = data.filter((value) =>
    value[indTerritorio].des == territorio &&
      value[indYear].des >= yearIni &&
      value[indCat].des == extra).map(
	  (value) => value[indice].val);
    if (reverse == 1) {
	serie = serie.reverse();
    }

  return serie;
}

function selecciona (data,ind) {
      let serie = data.slice(ind);
      return serie;
}
