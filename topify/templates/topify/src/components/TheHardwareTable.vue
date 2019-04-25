<template>
  <v-card>
    <v-data-table :items="items" hide-headers hide-actions class="elevation-1">
      <template v-slot:items="props">
        <td class="text-xs">{{ props.item.name }}</td>
        <td class="text-xs" width="50%">
          <v-progress-linear
            :value="props.item.percent"
            :color="props.item.color"
            height="5"
          />
        </td>
        <td class="text-xs">{{ props.item.percent }}%</td>
        <td v-if="props.item.total && props.item.used" class="text-xs">
          {{ byteFormat(props.item.used) }} /
          {{ byteFormat(props.item.total) }}
        </td>
        <td v-else-if="props.item.temperature" class="text-xs">
          {{ props.item.temperature }}°C
        </td>
        <td v-else class="text-xs" />
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
var _ = require("lodash");
export default {
  computed: {
    items() {
      let result = [];

      let cpu = this.$store.state.cpu;
      if (cpu.hasOwnProperty("percent_per_cpu")) {
        result.push(
          ...cpu.percent_per_cpu.map((percent, index) => {
            return {
              name: "Core " + index,
              percent: percent,
              color: "blue",
              temperature: _.get(
                cpu,
                "temperature_per_core[index].temperature_current"
              )
            };
          })
        );
      }

      let memory = this.$store.state.memory;
      result.push({
        name: "RAM",
        percent: _.get(memory, "ram.percent", "N/A"),
        color: "orange",
        total: _.get(memory, "ram.total", "N/A"),
        used: _.get(memory, "ram.used", "N/A")
      });
      result.push({
        name: "Swap",
        percent: _.get(memory, "swap.percent", "N/A"),
        color: "orange",
        total: _.get(memory, "swap.total", "N/A"),
        used: _.get(memory, "swap.used", "N/A")
      });
      return result;
    }
  },
  methods: {
    byteFormat: function(input) {
      let fileSizeInBytes = input;
      let i = -1;
      let byteUnits = [" kB", " MB", " GB", " TB", "PB", "EB", "ZB", "YB"];
      do {
        fileSizeInBytes = fileSizeInBytes / 1024;
        i++;
      } while (fileSizeInBytes > 1024);
      return Math.max(fileSizeInBytes, 0.1).toFixed(1) + byteUnits[i];
    }
  }
};
</script>
