<template>
  <v-card>
    <v-card-text class="pa-0">
      <v-container class="pa-0">
        <div class="layout row ma-0">
          <div class="sm6 xs6 flex" :class="color">
            <div class="layout column ma-0 justify-center align-center">
              <v-icon size="56px" color="white"> {{ icon }} </v-icon>
            </div>
          </div>
          <div
            class="sm6 xs6 flex text-sm-center py-3 white--text"
            :class="color"
          >
            <div class="headline bold">{{ title }}</div>
            <span class="caption"> {{ subTitle }} </span>
          </div>
        </div>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    icon: {
      type: String,
      default: ""
    },
    title: {
      type: String,
      default: ""
    },
    subTitle: {
      type: String,
      default: ""
    },
    color: {
      type: String,
      default: ""
    }
  }
};
</script>
