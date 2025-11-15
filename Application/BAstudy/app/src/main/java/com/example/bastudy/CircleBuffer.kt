package com.example.bastudy

class CircleBuffer(private val capacity: Int) {

    private var size: Int = 0
    private var pointer: Int = 0
    private var buffer: DoubleArray = DoubleArray(capacity)

    fun append(distance: Double){
        if(pointer == capacity){
            pointer = 0
        }
        buffer[pointer] = distance
        pointer++
        if(size < capacity){
            size++
        }
    }

    fun clearBuffer(){
        buffer = DoubleArray(capacity)
        size = 0
        pointer = 0
    }

    fun printBufferContent(){
        for (i in 0 until size){
            print("${buffer[i]} ")
        }
        println()
    }

    fun average(): Double {
        var sum: Double = 0.0
        for (i in 0 until size){
            sum += buffer[i]
        }
        if(size > 0){
            return sum/size
        } else{
            return 0.0
        }
    }

}