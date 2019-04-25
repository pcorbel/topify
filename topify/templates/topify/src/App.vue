<template>
  <v-app>
    <the-app-toolbar />
    <v-content>
      <router-view />
    </v-content>
    <the-bottom-nav />
  </v-app>
</template>

<script>
import TheAppToolbar from "@/components/TheAppToolbar";
import TheBottomNav from "@/components/TheBottomNav";
import axios from "axios";
export default {
  name: "App",
  components: {
    TheAppToolbar,
    TheBottomNav
  },
  created() {
    this.pollData();
  },
  beforeDestroy() {
    clearInterval(this.polling);
  },
  data() {
    return {
      polling: null
    };
  },
  methods: {
    pollData() {
      this.$store.dispatch("fetchData");
      axios
        .get(process.env.VUE_APP_ROOT_API + process.env.VUE_APP_ENDPOINT_ENV)
        .then(env => {
          this.polling = setInterval(() => {
            this.$store.dispatch("fetchData");
          }, Number(env.data.env.REFRESH_INTERVAL));
        });
    }
  }
};
</script>
