import NextAuth from "next-auth"
import Providers from "next-auth/providers"

const handler = NextAuth({
  providers: [
    Providers.Google({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET
    })
    // Otros proveedores pueden ir aquí
  ],
  // Otras configuraciones de NextAuth
})

export { handler as GET, handler as POST }
