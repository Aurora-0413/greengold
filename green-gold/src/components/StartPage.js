import backgroundImage from '../assets/images/1.png'

export default {
    name: 'StartPage',
    data() {
        return {
            backgroundImage
        }
    },
    methods: {
        startExplore() {
            this.$router.push('/main')
        }
    }
}