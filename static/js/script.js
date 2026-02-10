function display_AI_Insights(MODEL_OUTPUT){
  const type= MODEL_OUTPUT.type
  insight_card=document.getElementById(type).querySelector(".insights");
  insight_card.innerHTML=`<p>${MODEL_OUTPUT.ai_insight}</p>`
  insight_card.style.display="block"
}

// Object to store chart instances to prevent overlapping/glitching
let chartInstances = {};

// Mapping of chart IDs to their respective analysis modes
const MODE_CHART_MAP = {
  single: ["spiderChart"],
  batch: ["academicBar", "personaBar", "steadyPie", "improvedPie", "decliningPie"]
};

// Destroys charts specific to the provided mode.
function clear_canvas(type) {
  const chartsToClear = MODE_CHART_MAP[type] || [];

  chartsToClear.forEach(id => {
    if (chartInstances[id]) {
      chartInstances[id].destroy();
      delete chartInstances[id]; // Remove reference from the object
    }
  });
}

// renders charts
function render_charts(MODEL_OUTPUT) {
  // displaying  the charts
  document.getElementById(MODEL_OUTPUT.type).style.display="block"

  // start with cleaning canvas 
  clear_canvas(MODEL_OUTPUT.type)
  

  if (MODEL_OUTPUT.type==="single"){
      // logic for spider charts
      // single student score value 
      if (MODEL_OUTPUT.is_predicted){
      document.getElementById(MODEL_OUTPUT.type).getElementsByTagName[0].style.display="block";
      document.getElementById("predictedScore").innerText = MODEL_OUTPUT.score_value;
      }
      //  spider chart
      chartInstances["spiderChart"]=new Chart(document.getElementById("spiderChart"), {
          type: "radar",
          data: {
              labels: MODEL_OUTPUT.charts.spider_chart.data.map(d => d.subject),
              datasets: [{
                label: "Student Profile",
                data: MODEL_OUTPUT.charts.spider_chart.data.map(d => d.value),
                fill: true
              }]
            },
          options: {
              scales: {
                r: { min: 0, max: 100 }
              }
            }
          });
              }


   else if (MODEL_OUTPUT.type === "batch") {
    // render new charts

    // Render Academic Bar
    chartInstances["academicBar"] = new Chart(document.getElementById("academicBar"), {
      type: "bar",
      data: {
        labels: MODEL_OUTPUT.charts.academic_distribution.map(d => d.name),
        datasets: [{
          label: "Students",
          data: MODEL_OUTPUT.charts.academic_distribution.map(d => d.value),
          backgroundColor: ['#F5F227','#27F579', '#F20A22']
        }]
      },
      options: {indexAxis: 'y' ,
          plugins: {
            tooltip: {
              callbacks: {
                label: ctx =>
                  `${ctx.raw} students (${MODEL_OUTPUT.charts.academic_distribution[ctx.dataIndex].percentage}%)`
              }
            }
          }
        }
      });
  

    // Render Persona Bar (Horizontal)
    chartInstances["personaBar"] = new Chart(document.getElementById("personaBar"), {
      type: "bar",
      data: {
        labels: MODEL_OUTPUT.charts.overall_persona_distribution.map(d => d.name),
        datasets: [{
          label: "Students",
          data: MODEL_OUTPUT.charts.overall_persona_distribution.map(d => d.value),
          backgroundColor: '#00c6ff'
        }]
      },

      options: {indexAxis: 'y',
          plugins: {
            tooltip: {
              callbacks: {
                label: ctx =>
                  `${ctx.raw} students (${MODEL_OUTPUT.charts.overall_persona_distribution[ctx.dataIndex].percentage}%)`
              }
            }
          }
        }
      });


    // Render Cluster Pies
    const pieCanvasIds = ["steadyPie", "improvedPie", "decliningPie"];
    const clusterEntries = Object.entries(MODEL_OUTPUT.charts.persona_per_academic_cluster);

    clusterEntries.forEach(([clusterName, personas], i) => {
      if (i >= pieCanvasIds.length) return;
      const canvasId = pieCanvasIds[i];
      chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
        type: "pie",
        data: {
          labels: personas.map(p => p.persona),
          datasets: [{
            data: personas.map(p => p.count)
          }]
        },
        options: {
            plugins: {
              tooltip: {
                callbacks: {
                  label: ctx =>
                    `${ctx.label}: ${ctx.raw} (${personas[ctx.dataIndex].percentage}%)`
                }
              }
            }
          }
        });
      });
          }
    

    // insights 
    display_AI_Insights(MODEL_OUTPUT)
}

