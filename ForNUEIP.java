/**
 *
 * @author Samuel, Luo
 *
 * 上機測驗-物件＆演算法
 *
 */

import java.util.Arrays;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

abstract class AbstractVehicle {
    protected abstract String getNumberOfTires();
    // 皆為交通工具、皆有輪胎
    public String intro(){
        return String.format("I am the vehicle. I have %s tires", getNumberOfTires());
    };
}

// 輪胎數有差異，分別實作
class Cars extends AbstractVehicle {
    @Override
    protected String getNumberOfTires(){
        return "4";
    }
}

// 輪胎數有差異，分別實作
class Scooters extends AbstractVehicle {
    @Override
    protected String getNumberOfTires(){
        return "2";
    }
}

public class ForNUEIP{
    public static int[] mergeSort(int[] arr) {
        int arrLen = arr.length;
        if (arrLen <= 1) return arr;
        int mid = (arrLen / 2);
        int left[] = new int[mid];
        int right[] = new int[arrLen - mid];
        System.arraycopy(arr, 0, left, 0, mid);
        System.arraycopy(arr, mid, right, 0, arrLen - mid);
        return merge(mergeSort(left), mergeSort(right));
    }

    public static int[] merge(int[] left, int[] right) {
        int[] res = new int[left.length + right.length];
        int l = 0, r = 0, res_idx = 0;
        while (l < left.length && r < right.length) res[res_idx++] = (left[l] >= right[r]) ? right[r++] : left[l++];
        while (l < left.length) res[res_idx++] = left[l++];
        while (r < right.length) res[res_idx++] = right[r++];
        return res;
    }

    public static void main(String args[]) {
        // 一、物件導向-繼承/介面
        System.out.println(new Cars().intro());
        System.out.println(new Scooters().intro());

        // 二、資料處理-字串
        String str = "人易科技:上 機 測 驗 - 演算法";
        final char replaceChar = ':';
        // 改成全型
        str = str.replace(replaceChar, (char)(replaceChar + 65248));
        // 去掉空白
        str = str.replaceAll("(?<=[\\u4E00-\\u9FFF])\\s+(?=[\\u4E00-\\u9FFF])", "");
        // 列印
        System.out.println(str.substring(str.indexOf('：') + 1, str.indexOf('-') - 1));

        // 三、資料處理-陣列
        int[] arr = new int[]{0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
        // 奇總 - 偶總
        int oddSum = 0, evenSum = 0;
        for (int el : arr) {
            if (el % 2 != 0) oddSum++;
            else evenSum++;
        }
        System.out.println(oddSum - evenSum);
        // 分割成二陣列
        int[] oddArr = new int[oddSum];
        int[] evenArr = new int[evenSum];
        int oddTmp = 0, evenTmp = 0;
        for (int el : arr) {
            if (el % 2 != 0) oddArr[oddTmp++] = el;
            else evenArr[evenTmp++] = el;
        }
        System.out.println(Arrays.toString(oddArr));
        System.out.println(Arrays.toString(evenArr));

        // 四、資料排序-正序
        int[] unsortedArr = new int[]{77, 5, 5, 22, 13, 55, 97, 4, 796, 1, 0, 9};
        System.out.println(Arrays.toString(mergeSort(unsortedArr)));

        // 五、邏輯處理-交集、差集、聯集
        Integer[] arrA = new Integer[]{77, 5, 5, 22, 13, 55, 97, 4, 796, 1, 0, 9};
        Integer[] arrB = new Integer[]{0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
        Set<Integer> set = new HashSet<Integer>(Arrays.asList(arrA.length > arrB.length ? arrA : arrB));
        Integer[] shorterArr = arrA.length > arrB.length ? arrB : arrA;

        // 交集
        List<Integer> arrList = new ArrayList<Integer>();
        for (Integer el : shorterArr) if (set.contains(el)) arrList.add(el);
        Integer[] arrC = arrList.toArray(new Integer[0]);
        System.out.println(Arrays.toString(arrC));

        // 差集
        Set<Integer> setCopy = set;
        for (Integer el : shorterArr) {
            if (set.contains(el)) setCopy.remove(el);
            else setCopy.add(el);
        }
        Integer[] arrD = setCopy.toArray(new Integer[0]);
        System.out.println(Arrays.toString(arrD));

        // 聯集
        Set<Integer> setCopy2 = set;
        for (Integer el : shorterArr) {
            if (!set.contains(el)) setCopy2.add(el);
        }
        Integer[] arrE = setCopy2.toArray(new Integer[0]);
        System.out.println(Arrays.toString(arrE));

    }
}