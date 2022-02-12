class FenwickTree:
    """
    Fenwick / Binary Indexed Tree (BIT).
    Based on the excellent video series:
    https://www.youtube.com/watch?v=RgITNht_f4Q

    Author: https://github.com/BlueBlazin
    """

    def __init__(self, nums: list[int | float]):
        """
        Converts `nums` into a Fenwick tree in linear time.
        **Note:** only a shallow copy is performed over the list.

        Args:
            nums: the list of numbers to convert.
        """
        self._tree = nums.copy()
        self._lsb = []
        # compute rightmost set bit for each index in [1, n]
        for n in range(1, len(nums) + 1):
            b = 1
            while n & 1 != 1:
                n >>= 1
                b <<= 1
            self._lsb.append(b)
        # turn `self._tree` into a BIT in-place
        self._make_tree()

    def _make_tree(self):
        n = len(self._tree)

        for i in range(1, n + 1):
            j = i + self._lsb[i - 1]

            if j <= n:
                self._tree[j - 1] += self._tree[i - 1]

    def prefix_sum(self, index: int) -> int | float:
        """
        Calculate the sum (in the original list) of all
        elements up-to and including `index` in O(log N) time.

        Args:
            index: index in the original list up to which the sum is computed.

        Returns:
            The sum of elements up-to and including `index`.
        """
        # use i = index + 1 since BITs are 1 indexed but the API is 0 indexed
        res, i = 0, index + 1

        while i > 0:
            res += self._tree[i - 1]
            i -= self._lsb[i - 1]
        return res

    def range_sum(self, left: int, right: int) -> int | float:
        """
        Calculates the sum (in the original list) of all elements
        in the closed range [left, right] in O(log N) time.

        Args:
            left: the start index of the range.
            right: the end index (inclusive) of the range

        Returns:
            The sum of all elements in the range.
        """
        right = self.prefix_sum(right)
        left = self.prefix_sum(left - 1) if left > 0 else 0

        return right - left

    def update(self, index: int, val: int | float) -> int | float:
        """
        Updates the value at `index` in the original list in O(log N) time.

        Args:
            index: the index in the original list to modify.
            val: the new value to set at `index`.
        """
        x = val - self.range_sum(index, index)
        i = index + 1

        while i <= len(self._tree):
            self._tree[i - 1] += x
            i += self._lsb[i - 1]


if __name__ == "__main__":
    tree = FenwickTree([9, -8])
    tree.update(0, 3)
    print(tree.range_sum(1, 1))
