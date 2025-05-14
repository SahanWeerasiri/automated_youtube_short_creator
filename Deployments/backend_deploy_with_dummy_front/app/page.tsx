"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function Home() {
  const [radius, setRadius] = useState<number>(5)
  const [result, setResult] = useState<string>("")
  const [helloMessage, setHelloMessage] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(false)

  const fetchHello = async () => {
    setLoading(true)
    try {
      const response = await fetch("/api/hello")
      const data = await response.json()
      setHelloMessage(data.message)
    } catch (error) {
      setHelloMessage("Error fetching hello message")
    } finally {
      setLoading(false)
    }
  }

  const calculateRadius = async () => {
    setLoading(true)
    try {
      const response = await fetch("/api/calculate_radius", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ r: radius }),
      })
      const data = await response.json()
      setResult(`Area: ${data.area.toFixed(2)}, Circumference: ${data.circumference.toFixed(2)}`)
    } catch (error) {
      setResult("Error calculating radius")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-24">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Next.js API Examples</CardTitle>
          <CardDescription>Test the API endpoints</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="hello" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="hello">/api/hello</TabsTrigger>
              <TabsTrigger value="radius">/api/calculate_radius</TabsTrigger>
            </TabsList>
            <TabsContent value="hello" className="space-y-4">
              <div className="mt-4">
                <p className="text-sm text-muted-foreground mb-2">Simple GET endpoint that returns a hello message.</p>
                <Button onClick={fetchHello} disabled={loading} className="w-full">
                  {loading ? "Loading..." : "Fetch Hello Message"}
                </Button>
                {helloMessage && (
                  <div className="mt-4 p-3 bg-muted rounded-md">
                    <p className="font-mono text-sm">{helloMessage}</p>
                  </div>
                )}
              </div>
            </TabsContent>
            <TabsContent value="radius" className="space-y-4">
              <div className="mt-4">
                <p className="text-sm text-muted-foreground mb-2">
                  POST endpoint that calculates area and circumference from radius.
                </p>
                <div className="flex items-center space-x-2 mb-4">
                  <Input
                    type="number"
                    value={radius}
                    onChange={(e) => setRadius(Number(e.target.value))}
                    placeholder="Enter radius"
                  />
                </div>
                <Button onClick={calculateRadius} disabled={loading} className="w-full">
                  {loading ? "Calculating..." : "Calculate"}
                </Button>
                {result && (
                  <div className="mt-4 p-3 bg-muted rounded-md">
                    <p className="font-mono text-sm">{result}</p>
                  </div>
                )}
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
        <CardFooter className="flex justify-between">
          <p className="text-xs text-muted-foreground">API endpoints: /api/hello and /api/calculate_radius</p>
        </CardFooter>
      </Card>
    </main>
  )
}
