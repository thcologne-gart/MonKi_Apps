<template>
  <v-breadcrumbs 
    :items="breadcrumbs"
    class="custom-breadcrumbs">
    <template v-slot:title="{ item }">
      <v-chip
        v-if="item.title !== ''"
        variant="outlined"
        style="background-color: whitesmoke;"
        color="highlight"
        link
        size="large"
        class="custom-chip">
        {{ item.title }}
      </v-chip>
    </template>
    <template v-slot:divider>
      <span class="custom-divider">&#8212;</span>
    </template>
  </v-breadcrumbs>
</template>

<script>
export default {
  data() {
    return {
      breadcrumbs: [],
    };
  },
  watch: {
    $route: 'generateBreadcrumbs',
  },
  created() {
    this.generateBreadcrumbs();
  },
  methods: {
  generateBreadcrumbs() {
    //console.log(this.$route)
    //console.log(this.$route.meta.breadcrumb(this.$route))
    this.breadcrumbs = this.$route.meta.breadcrumb(this.$route)
  },
  },
};
</script>

<style>
.custom-breadcrumbs {
  display: flex;
  align-items: center;
}

.custom-breadcrumbs a:hover {
  text-decoration: none !important;
}

.custom-chip {
  margin: 0;
}

.custom-divider {
  width: 100%; /* Set the width to 100% to span the entire width */
  text-align: center; /* Optional: Center the text within the divider */
}
.v-breadcrumbs-divider {
  padding-left: 0px !important;
  padding-right: 0px !important;
}
</style>
  
  