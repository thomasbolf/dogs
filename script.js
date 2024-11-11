const svg = d3
  .select("#d3-container")
//  .select("body")
  .append("svg")
  .attr("width","100%")
  .attr("height", "100%");

const x = d3
  .scaleLinear()
  .domain([2.6, 75.1])
  .rangeRound([600, 860]);

const color = d3
  .scaleThreshold()
  .domain(d3.range(2.6, 75.1, (75.1 - 2.6) / 8))
  .range(d3.schemeBlues[9]);



const tooltip = d3
  .select("body")
  .append("div")
  .attr("class", "tooltip")
  .attr("id", "tooltip")
  .style("opacity", 0);

const unemployment = d3.map();

const path = d3.geoPath();


Promise.all([
    d3.json("https://raw.githubusercontent.com/no-stack-dub-sack/testable-projects-fcc/master/src/data/choropleth_map/counties.json"),
    d3.csv("http://127.0.0.1:5001/counties") //dog data
]).then(([us, dogs]) => {
    ready(null, us, dogs);
}).catch(error => {
    console.error('Error loading data:', error);
});


function ready(error, us, dogs) {
    const dogData = new Map();
    dogs.forEach(d => {
      dogData.set(+d.county, +d.frequency); 
    });
    var texasCounties = topojson.feature(us, us.objects.counties).features.filter(function(d) {
        return d.id >= 48001 && d.id <= 48999;
      });    
    const g = svg.append("g")
      .attr("transform", "translate(210,-870)rotate(-3)");
     g
    .append("g")
    .attr("class", "counties")
    .selectAll("path")
    .data(texasCounties)
    .enter()
    .append("path")
    .attr("class", "county")
    .attr("data-fips", d => d.id)
    .attr("fill", d => {
        console.log(d.id);
        const value = dogData.get(d.id);
        return value ? color(value) : "#ccc"; // Use color scale if value exists, else gray
      })
    .attr("d", path)
    .attr("transform", "scale(3)")
    .on("mouseout", function(d) {
      tooltip.style("opacity", 0);
    });
  svg
    .append("path")
    .datum(topojson.mesh(us, us.objects.states, (a, b) => a.id == "48"|| b=="48"))
    .attr("class", "states")
    .attr("d", path)
    .attr('transform' , 'rotate(-180, '+0+',' +0 +')') ;
}
