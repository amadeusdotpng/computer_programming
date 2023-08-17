import java.util.*;

public class Program
{
	public static int[] getArray(int n)
	{
		int[] nums=new int[n];
		for(int i=0;i<nums.length;i++)
		{
			nums[i]=(int)(Math.random()*100);
		}
		return nums;
	}
	
	public static void radixSort(int[] nums)
	{
		int base=4;
		int baseToSomePower=1;
		LinkedList<Integer>[] buckets=new LinkedList[base];
		for(int i=0;i<base;i++)buckets[i]=new LinkedList<Integer>();
		for(int num:nums)
		{
			buckets[(num/baseToSomePower)%base].add(num);
		}
		baseToSomePower*=base;
		while(baseToSomePower>0) 
		{
			
			LinkedList<Integer>[] newbuckets=new LinkedList[base];
			for(int i=0;i<base;i++)newbuckets[i]=new LinkedList<Integer>();
			for(int i=0;i<base;i++)
				for(Integer num:buckets[i])
					newbuckets[(num/baseToSomePower)%base].add(num);
			buckets=newbuckets;
			baseToSomePower*=base;
		}
		
		int j=0;
		for(int i=0;i<base;i++)
			for(Integer num:buckets[i]) nums[j++]=num;
		
	}
	
	public static int[] zip(int[] a, int[] b)
	{
		int[] out=new int[a.length+b.length];
		int i=0,j=0;
		while(i<a.length && j<b.length)out[i+j]=a[i]<b[j]?a[i++]:b[j++];
		for(;i<a.length;i++)out[i+j]=a[i];
		for(;j<b.length;j++)out[i+j]=b[j];
		return out;
		
	}
	
	public static void main(String[] args)
	{
		int[] a=getArray(10);
		int[] b=getArray(10);
		System.out.println(Arrays.toString( a) );
		radixSort(a);
		radixSort(b);
		System.out.println(Arrays.toString( a) );
		System.out.println(Arrays.toString( b) );
		int[] z=zip(a,b);
		
		System.out.println(Arrays.toString( z) );
	}
}

//Selection,insertion, bubble   O(n*n)
//Radix  O(n*d)
//Quicksort
//Merge


//~ def mergesort(m):
	//~ a,b=split(m)
	//~ if len(a)>1 a=mergesort(a)
	//~ if len(b)>1 b=mergesort(b)
	//~ m=zip(a,b)
	//~ return m
qsort
	if list small then done
	while(L!=R)
		If nums[L] is less than pivot L++
		else if nums[R] is greater than pivot R--
		else swap(L,R)
	qsort(OGL,L-1)
	qsort(L+1,OGR)

 pivot_value=35
 
               L                           
[2, 26, 6, 1, 35, 40, 87, 63, 74, 64]
               R
