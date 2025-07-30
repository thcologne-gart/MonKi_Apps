<template>
    <div>
        <v-card
            style="border-radius: 20px; background-color: whitesmoke"
            class="pa-4" variant="outlined">
            <v-img v-if="this.grundfunktionId == 'Wärme versorgen'" src="@/assets/Gebäude Heizung On.svg"></v-img>
            <v-img v-else-if="this.grundfunktionId == 'Luft versorgen'" src="@/assets/Gebäude Lüftung On.svg"></v-img>
            <v-img v-else src="@/assets/Gebäude Alles Off.svg"></v-img>
        </v-card>
    </div>
</template>

<script>

export default{
    props: {
        grundfunktionId: String
    }
}

</script>

<style scoped>
.building-card {
  background-color: #ffffff;
}
</style>