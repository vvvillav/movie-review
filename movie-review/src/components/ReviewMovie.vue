<template>
  <b-card class="mt-2 principal">
    <!-- Filtros de búsqueda -->
    <b-row class="mt-2">
      <b-col md="4">
        <b-form-group>
          <b-form-input label= "Product" v-model="productId" placeholder="Buscar por productid" type="text" class="d-inline-block" />
        </b-form-group>
      </b-col>

      <b-col md="4">
        <b-form-group>
          <b-form-input v-model="userId" placeholder="Buscar por userid" type="text" class="d-inline-block" />
        </b-form-group>
      </b-col >
      
      <b-col md="2" class="mb-2 d-flex align-items-center justify-content-center">
        <datepicker v-model="fecha_desde" placeholder="Fecha desde"></datepicker>
      </b-col>

      <b-col md="2" class="mb-2 d-flex align-items-center justify-content-center">
        <datepicker v-model="fecha_hasta" placeholder="Fecha hasta"></datepicker>
      </b-col>
    </b-row>

    
    
    <!-- Botón de búsqueda -->
    <b-row >
      <b-col  class="d-flex justify-content-center">
        <b-button @click="fetch" class="mt-2 btn-sm">Buscar</b-button>
      </b-col>
    </b-row>

     <!-- Estadísticas -->
     <b-card-group class="mt-2">
      <b-card title="Valor Máximo Score" class="text-center">
        <p class="mb-0">{{ maxScore }}</p>
      </b-card>
      <b-card title="Valor Mínimo Score" class="text-center">
        <p class="mb-0">{{ minScore }}</p>
      </b-card>
      <b-card title="Conteo de Usuarios" class="text-center">
        <p class="mb-0">{{ userCount }}</p>
      </b-card>
      <b-card title="Promedio Score" class="text-center">
        <p class="mb-0">{{ promScore }}</p>
      </b-card>
    </b-card-group>
    <!-- Gráfico de visualización -->
    <b-row class="mt-2">
      <h2>VISUALIZACION</h2>
      <ChartVisualization v-if="chartData" ref="chartVisualization" :chartData="chartData" />
    </b-row>
    <!-- Tablas de revisiones -->
    <b-row class="mt-2">
      <b-col>
        <h3>top 10 best reviews:</h3>
        <b-table striped hover :items="reviewstop10b" :fields="fields"></b-table>
      </b-col>
    </b-row>
    
    <b-row class="mt-2">
      <b-col>
        <h3>top 10 worst reviews:</h3>
        <b-table striped hover :items="reviewstop10w" :fields="fields"></b-table>
      </b-col>
    </b-row>

    <b-row class="mt-2">
      <b-col>
        <h3>200 reviews:</h3>
        <b-table striped hover :items="reviews200" :fields="fields"></b-table>
      </b-col>
    </b-row>
  </b-card>
</template>


<script>

import { BCard, BTable, BRow, BCol, BButton, BFormGroup, BFormInput } from 'bootstrap-vue';
import axios from 'axios';  // Asegúrate de que axios esté instalado con npm
import Datepicker from 'vuejs-datepicker';
import ChartVisualization from './ChartVisualization.vue'


export default {
  components: {
     BTable, BRow, BCol, BButton, BFormGroup, BFormInput, Datepicker, ChartVisualization,BCard
  },
  data() {
    return {
      userId: '',
      productId: '',
      reviewstop10b: [],
      reviewstop10w: [],
      reviews200: [],
      reviewsFilterData: [],
      chartData: null,
      chartOptions: null,

      fields: ['productid', 'score', 'summary', 'reviewtext', 'userid'],
      fecha_desde: 0,
      fecha_hasta: 0,
      configdateTimePicker: {
        enableTime: false,
        dateFormat: 'd/m/Y',
      },

      maxScore: null,
      minScore: null,
      userCount: null,
      promScore: null,
    };
  },


  watch: {
    reviewsFilterData() {
      this.prepareChartData();
    }
  },



  methods: {


    fetch() {
      this.fetchScoreMaxMin();
      this.fetchPromScore();
      this.fetchCountUser();
      this.fetchtop10best();
      this.fetchtop10worst();
      this.fetchReviews200();
      this.fetchReviewsFilter();
    },
    prepareChartData() {
      // Asegúrate de que hay datos disponibles
      if (this.reviewsFilterData && this.reviewsFilterData.length > 0) {
        // Preparar los datos para el gráfico
        this.chartData = {
          type: "line",
          data: {
            labels: this.reviewsFilterData.map(item => item.reviewDate), // Las etiquetas son las fechas
            datasets: [
              {
                label: 'Average Score',
                backgroundColor: 'rgba(255, 99, 132, 0.2)', // Color de fondo para la línea de puntuación media
                borderColor: 'rgba(255, 99, 132, 1)', // Color del borde para la línea de puntuación media
                data: this.reviewsFilterData.map(item => item.averageScore), // Datos de puntuación media
                yAxisID: 'y-axis-1',
              },
              {
                label: 'Average Helpfulness',
                backgroundColor: 'rgba(54, 162, 235, 0.2)', // Color de fondo para la línea de utilidad media
                borderColor: 'rgba(54, 162, 235, 1)', // Color del borde para la línea de utilidad media
                data: this.reviewsFilterData.map(item => item.averageHelpfulness), // Datos de utilidad media
                yAxisID: 'y-axis-2',
              }
            ]
          },
          options: {
            responsive: true,
            lineTension: 1,
            scales: {
              yAxes: [
                {
                  id: 'y-axis-1',
                  type: 'linear',
                  position: 'left',
                  ticks: {
                    beginAtZero: true
                  }
                },
                {
                  id: 'y-axis-2',
                  type: 'linear',
                  position: 'right',
                  ticks: {
                    beginAtZero: true
                  },
                  gridLines: {
                    drawOnChartArea: false
                  }
                }
              ]
            }
          }
        };

      } else {
        // Si no hay datos, puedes establecer valores predeterminados o dejarlos vacíos
        this.chartData = null;
        this.chartOptions = null;
      }
      console.log("CHART::", this.chartData)
      //this.$refs.chartVisualization.updateChartData(this.chartData);
    },
    fetchReviewsFilter() {
      const variables = {};
      if (this.userId) variables.userID = this.userId;
      if (this.productId) variables.productID = this.productId;
      if (this.fecha_desde) variables.startDate = this.convertDateToMinutes(this.fecha_desde);
      if (this.fecha_hasta) variables.endDate = this.convertDateToMinutes(this.fecha_hasta);

      const query = {
        query: `
            query GetReviewsFilter($productID: String, $userID: String, $startDate: Int, $endDate: Int) {
              reviewsFilter(productId: $productID, userId: $userID, startDate: $startDate, endDate: $endDate) {
                reviewDate
                averageScore
                averageHelpfulness
              }
            }
          `,
        variables
      };

      axios.post('http://localhost:8000/graphql/', query)
      .then(response => {
        this.reviewsFilterData = response.data.data.reviewsFilter;
        this.prepareChartData();
        })
        .catch(error => {
          console.error(error);
        });
    },


    fetchScoreMaxMin() {
      const variables = {};
      if (this.userId) variables.userID = this.userId;
      if (this.productId) variables.productID = this.productId;
      if (this.fecha_desde) variables.startDate = this.convertDateToMinutes(this.fecha_desde);
      if (this.fecha_hasta) variables.endDate = this.convertDateToMinutes(this.fecha_hasta);

      const query = {
        query: `
          query GetMaxMinScore($productID: String, $userID: String, $startDate: Int, $endDate: Int) {
            maxMinScore(productId: $productID, userId: $userID, startDate: $startDate, endDate: $endDate) {
              maxScore
              minScore
            }
          }
        `,
        variables
      };

      axios
        .post('http://localhost:8000/graphql/', query)
        .then((response) => {
          // Manejar la respuesta
          const data = response.data.data;
          console.log(data)
          this.maxScore = data.maxMinScore.maxScore;
          this.minScore = data.maxMinScore.minScore;
        })
        .catch((error) => {
          // Manejar el error
          console.error(error);
        });
    },
    fetchPromScore() {
      const variables = {};
      if (this.userId) variables.userID = this.userId;
      if (this.productId) variables.productID = this.productId;
      if (this.fecha_desde) variables.startDate = this.convertDateToMinutes(this.fecha_desde);
      if (this.fecha_hasta) variables.endDate = this.convertDateToMinutes(this.fecha_hasta);

      const query = {
        query: `
          query GetAverageScore($productID: String, $userID: String, $startDate: Int, $endDate: Int) {
            averageScore(productId: $productID, userId: $userID, startDate: $startDate, endDate: $endDate)
          }
        `,
        variables
      };

      axios
        .post('http://localhost:8000/graphql/', query)
        .then((response) => {
          this.promScore = response.data.data.averageScore;
        })
        .catch((error) => {
          // Manejar el error
          console.error(error);
        });
    },
    fetchCountUser() {
      const variables = {};
      if (this.userId) variables.userID = this.userId;
      if (this.productId) variables.productID = this.productId;
      if (this.fecha_desde) variables.startDate = this.convertDateToMinutes(this.fecha_desde);
      if (this.fecha_hasta) variables.endDate = this.convertDateToMinutes(this.fecha_hasta);

      const query = {
        query: `
        query GetUserCount($productID: String, $userID: String, $startDate: Int, $endDate: Int) {
          userCount(productId: $productID, userId: $userID, startDate: $startDate, endDate: $endDate)
        }

        `,
        variables
      };

      axios
        .post('http://localhost:8000/graphql/', query)
        .then((response) => {
          this.userCount = response.data.data.userCount;
        })
        .catch((error) => {
          // Manejar el error
          console.error(error);
        });
    },
    convertDateToMinutes(dateString) {
      const date = new Date(dateString);
      return Math.floor(date.getTime() / 1000); // Convierte la fecha a milisegundos y luego a segundos
    },

    fetchtop10worst() {
      const variables = {};
      if (this.userId) variables.userID = this.userId;
      if (this.productId) variables.productID = this.productId;
      if (this.fecha_desde) variables.startDate = this.convertDateToMinutes(this.fecha_desde);
      if (this.fecha_hasta) variables.endDate = this.convertDateToMinutes(this.fecha_hasta);

      const query = {
        query: `
            query GetTop10WorstScores($productID: String, $userID: String, $startDate: Int, $endDate: Int) {
              top10WorstScores(productId: $productID, userId: $userID, startDate: $startDate, endDate: $endDate) {
                productid
                userid
                profilename
                helpfulness
                score
                reviewtime
                summary
                reviewtext
              }
            }
            `,
        variables
      };

      axios.post('http://localhost:8000/graphql/', query)
        .then(response => {
          // Manejar la respuesta
          this.reviewstop10w = response.data.data.top10WorstScores;
        })
        .catch(error => {
          // Manejar el error
          console.error(error);
        });
    },
    fetchtop10best() {
      const variables = {};
      if (this.userId) variables.userID = this.userId;
      if (this.productId) variables.productID = this.productId;
      if (this.fecha_desde) variables.startDate = this.convertDateToMinutes(this.fecha_desde);
      if (this.fecha_hasta) variables.endDate = this.convertDateToMinutes(this.fecha_hasta);

      const query = {
        query: `
            query GetTop10BestScores($productID: String, $userID: String, $startDate: Int, $endDate: Int) {
              top10BestScores(productId: $productID, userId: $userID, startDate: $startDate, endDate: $endDate) {
                productid
                userid
                profilename
                helpfulness
                score
                reviewtime
                summary
                reviewtext
              }
            }

            `,
        variables
      };

      axios.post('http://localhost:8000/graphql/', query)
        .then(response => {
          // Manejar la respuesta
          this.reviewstop10b = response.data.data.top10BestScores;
        })
        .catch(error => {
          // Manejar el error
          console.error(error);
        });
    },
    fetchReviews200() {
      const variables = {};
      if (this.userId) variables.userID = this.userId;
      if (this.productId) variables.productID = this.productId;
      if (this.fecha_desde) variables.startDate = this.convertDateToMinutes(this.fecha_desde);
      if (this.fecha_hasta) variables.endDate = this.convertDateToMinutes(this.fecha_hasta);

      const query = {
        query: `
          query GetFirst200Reviews($productID: String, $userID: String, $startDate: Int, $endDate: Int) {
            first200Reviews(productId: $productID, userId: $userID, startDate: $startDate, endDate: $endDate) {
              productid
              userid
              profilename
              helpfulness
              score
              reviewtime
              summary
              reviewtext
            }
          }
          `,
        variables
      };

      axios.post('http://localhost:8000/graphql/', query)
        .then(response => {
          // Manejar la respuesta
          this.reviews200 = response.data.data.first200Reviews;
        })
        .catch(error => {
          // Manejar el error
          console.error(error);
        });
    },
  }




}

</script>
<style>
  .centered-datepicker {
    display: flex;
    justify-content: center;
  }
  .custom-centered {
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>