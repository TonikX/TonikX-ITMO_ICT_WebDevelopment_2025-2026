class Solution13 {
    fun romanToInt(s: String): Int {
        val map = mapOf(
            'I' to 1,
            'V' to 5,
            'X' to 10,
            'L' to 50,
            'C' to 100,
            'D' to 500,
            'M' to 1000
        )

        var result = 0

        for (i in s.indices) {
            val value = map[s[i]]!!

            if (i < s.length - 1 && value < map[s[i + 1]]!!) {
                result -= value
            } else {
                result += value
            }
        }

        return result
    }
}