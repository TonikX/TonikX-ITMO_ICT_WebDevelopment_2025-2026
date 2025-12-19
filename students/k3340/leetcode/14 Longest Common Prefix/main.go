package main

func longestCommonPrefix(strs []string) string {
	minLen := len(strs[0])
	for _, s := range strs {
		if len(s) < minLen {
			minLen = len(s)
		}
	}

	prefix := ""
	for i := 0; i < minLen; i++ {
		currChar := strs[0][i]
		for _, s := range strs {
			if s[i] != currChar {
				return prefix
			}
		}
		prefix += string(currChar)
	}

	return prefix
}
