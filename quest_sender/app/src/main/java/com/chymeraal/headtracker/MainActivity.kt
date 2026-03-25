package com.chymeraal.headtracker

import android.app.Activity
import android.hardware.display.DisplayManager
import android.os.Bundle
import android.view.Display
import android.view.WindowManager
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress

class MainActivity : Activity() {

    private var udpSocket: DatagramSocket? = null
    private var senderThread: Thread? = null
    private var running = false

    // Remplace par l'IP de ton PC Linux sur le réseau WiFi
    private val pcIp = "192.168.1.XXX"   // ←←← CHANGE ÇA !!!
    private val udpPort = 5005

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        setContentView(R.layout.activity_main)  // on va créer un layout minimal

        try {
            udpSocket = DatagramSocket()
            startSending()
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun startSending() {
        running = true
        senderThread = Thread {
            val buffer = ByteArray(128)
            val address = InetAddress.getByName(pcIp)

            while (running) {
                try {
                    val display = getSystemService(DISPLAY_SERVICE) as DisplayManager
                    val pose = display.getDisplay(Display.DEFAULT_DISPLAY).getPose() // API Meta Quest

                    val q = pose.quaternion  // x, y, z, w

                    val msg = "${q.x},${q.y},${q.z},${q.w}"
                    val packet = DatagramPacket(msg.toByteArray(), msg.length, address, udpPort)
                    udpSocket?.send(packet)

                    Thread.sleep(20) // ~50 Hz
                } catch (e: Exception) {
                    Thread.sleep(100)
                }
            }
        }
        senderThread?.start()
    }

    override fun onDestroy() {
        running = false
        senderThread?.interrupt()
        udpSocket?.close()
        super.onDestroy()
    }
}
