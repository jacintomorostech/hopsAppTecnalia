from flask import Flask
import ghhops_server as hs
import rhino3dm

###fjfhe
# register hops app as middleware
app = Flask(__name__)
hops: hs.HopsFlask = hs.Hops(app)

@hops.component(
    "/mergesort",
    name="Merge Sort",
    nickname="MergeSort",
    description="Merge sort algorithm",
    inputs=[
        hs.HopsNumber("List", "L", "List of numbers to sort", access = hs.HopsParamAccess.LIST)
    ],
    outputs=[hs.HopsNumber("List", "L", "Sorted list of numbers")]
)
def merge_sort(list: list):
    if len(list) > 1:
        mid = len(list) // 2
        left = list[:mid]
        right = list[mid:]
        merge_sort(left)
        merge_sort(right)
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                list[k] = left[i]
                i += 1
            else:
                list[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            list[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            list[k] = right[j]
            j += 1
            k += 1
    return list

if __name__ == "__main__":
    app.run(debug=True)