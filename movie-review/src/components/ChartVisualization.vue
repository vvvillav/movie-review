<template>
  <div>
    <canvas id="canvas"></canvas>
  </div>
</template>

<script>

import Chart from 'chart.js/auto';

export default {
  name: 'CharVisualization',
  props: ['chartData'],
  data() {
    return {
      movieChartData: {}
    }
  },
  methods: {
    updateChartData(data) {
      const dt = JSON.stringify(data);
      console.log("DAT::", JSON.parse(dt))
      //this.movieChartData = JSON.parse(dt);
      this.movieChartData = this.chartData
    }
  },
  mounted() {
    const ctx = document.getElementById('canvas');
    console.log("MOV::", this.movieChartData)
    console.log("CHR::", this.chartData)
    new Chart(ctx, this.chartData);
  }
}
</script>

