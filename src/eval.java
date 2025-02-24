package com.example1;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class EvalTest {

    @Test
    public void testCountElementsPromptArray() {
        System.out.println("countElements");
        int[] A = {7, 14, 21, 28, 35, 42, 49, 56, 63, 70};
        int expResult = 8;
        int result = DivisibleBy7WithGreaterElements.countElements(A);
        assertEquals(expResult, result);
    }

    @Test
    public void testCountElementsMixedArray() {
        System.out.println("countElements");
        int[] A = {14, 1, 4, -6, 3, 8};
        int expResult = 0;
        int result = DivisibleBy7WithGreaterElements.countElements(A);
        assertEquals(expResult, result);
    }

    @Test
    public void testCountElementsEmptyArray() {
        System.out.println("countElements");
        int[] A = {};
        int expResult = 0;
        int result = DivisibleBy7WithGreaterElements.countElements(A);
        assertEquals(expResult, result);
    }
}