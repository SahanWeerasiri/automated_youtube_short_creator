import { NextResponse } from "next/server"

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { r } = body

    if (typeof r !== "number") {
      return NextResponse.json({ error: "Radius must be a number" }, { status: 400 })
    }

    const area = Math.PI * r * r
    const circumference = 2 * Math.PI * r

    return NextResponse.json({ area, circumference })
  } catch (error) {
    return NextResponse.json({ error: "Invalid request body" }, { status: 400 })
  }
}
