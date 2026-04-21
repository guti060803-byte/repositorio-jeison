import flet as ft
import asyncio


class PortafolioHacker:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Jeison Gutierrez v1.0"
        self.page.padding = 0
        self.page.bgcolor = "#0d0f18"
        self.page.theme_mode = ft.ThemeMode.DARK

        # === PALETA ===
        self.c_bg        = "#0d0f18"
        self.c_surface   = "#13111e"
        self.c_surface2  = "#1a1730"
        self.c_border    = "#1f1d2e"
        self.c_violet    = "#7c3aed"
        self.c_violet_lt = "#a78bfa"
        self.c_neon      = "#00FF41"   # solo para terminal
        self.c_text      = "#f1f5f9"
        self.c_muted     = "#475569"
        self.c_dimmed    = "#2d3148"

        # Elementos animados
        self.titulo_nombre = ft.Text(
            "", size=58, weight="bold",
            color=self.c_text,
            font_family="monospace",
        )
        self.status_text = ft.Text(
            "", color=self.c_violet_lt, size=11, font_family="monospace"
        )
        self.log_terminal = ft.Column(spacing=2)

        self.build()

    # ─────────────────────────────────────────
    #  COMPONENTES
    # ─────────────────────────────────────────

    def badge(self, texto):
        return ft.Container(
            content=ft.Text(texto, size=11, color=self.c_violet_lt, font_family="monospace"),
            bgcolor="#1a0f38",
            border=ft.border.all(0.5, "#4c2e8a"),
            border_radius=100,
            padding=ft.padding.symmetric(vertical=5, horizontal=14),
        )

    def skill_tag(self, texto):
        return ft.Container(
            content=ft.Row(
                spacing=6,
                controls=[
                    ft.Container(width=6, height=6, border_radius=3, bgcolor=self.c_violet_lt),
                    ft.Text(texto, size=11, color=self.c_muted),
                ],
            ),
            bgcolor="#0f0e1a",
            border=ft.border.all(0.5, self.c_border),
            border_radius=6,
            padding=ft.padding.symmetric(horizontal=10, vertical=4),
        )

    def card(self, titulo, texto, icono_src=None, url=None):
        def hover(e):
            e.control.bgcolor = self.c_surface2 if e.data == "true" else self.c_surface
            e.control.border = ft.border.all(
                1 if e.data == "true" else 0.5,
                self.c_violet_lt if e.data == "true" else self.c_border,
            )
            e.control.update()

        if icono_src:
            icono_widget = ft.Container(
                content=ft.Image(src=icono_src, width=26, height=26, color=self.c_violet_lt),
                width=42, height=42,
                bgcolor="#1a0f38",
                border_radius=10,
                alignment=ft.Alignment(0, 0),
            )
        else:
            icono_widget = ft.Container(
                content=ft.Text("{  }", color=self.c_violet_lt, size=14, font_family="monospace"),
                width=42, height=42,
                bgcolor="#1a0f38",
                border_radius=10,
                alignment=ft.Alignment(0, 0),
            )

        return ft.Container(
            width=820,
            padding=ft.padding.symmetric(horizontal=16, vertical=14),
            bgcolor=self.c_surface,
            border=ft.border.all(0.5, self.c_border),
            border_radius=12,
            on_hover=hover,
            on_click=(lambda _: self.page.launch_url(url)) if url else None,
            content=ft.Row(
                spacing=16,
                vertical_alignment="center",
                controls=[
                    icono_widget,
                    ft.Column(
                        spacing=3,
                        expand=True,
                        controls=[
                            ft.Text(titulo, weight="bold", color=self.c_text, size=15),
                            ft.Text(texto, color=self.c_muted, size=12),
                        ],
                    ),
                    ft.Text("›", color=self.c_dimmed, size=20),
                ],
            ),
        )

    def skill(self, nombre, valor):
        pct = int(valor * 100)
        return ft.Column(
            spacing=6,
            controls=[
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Text(f"> {nombre}", color=self.c_muted, size=13, font_family="monospace"),
                        ft.Text(f"{pct}%", color=self.c_violet_lt, size=12, font_family="monospace"),
                    ],
                ),
                ft.Stack(
                    height=3,
                    controls=[
                        ft.Container(width=780, height=3, border_radius=2, bgcolor=self.c_dimmed),
                        ft.Container(width=int(780 * valor), height=3, border_radius=2, bgcolor=self.c_violet_lt),
                    ],
                ),
            ],
        )

    def section_header(self, texto):
        return ft.Row(
            controls=[
                ft.Text(texto, size=22, weight="bold", color=self.c_violet_lt, font_family="monospace"),
                ft.Container(expand=True, height=1, bgcolor=self.c_border),
            ],
            spacing=16,
            vertical_alignment="center",
        )

    # ─────────────────────────────────────────
    #  BUILD
    # ─────────────────────────────────────────

    def build(self):

        # ── NAVBAR ──────────────────────────
        self.navbar = ft.Container(
            bgcolor="#09090f",
            padding=ft.padding.symmetric(horizontal=32, vertical=14),
            border=ft.border.only(bottom=ft.border.BorderSide(0.5, "#2e1f5e")),
            content=ft.Row(
                alignment="spaceBetween",
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Image(src="noni.svg", width=24, height=24, color=self.c_violet_lt),
                            ft.Text("👑JAG👑", color=self.c_violet_lt, weight="bold", size=18, font_family="monospace"),
                        ],
                    ),
                    ft.Row([
                        ft.TextButton("inicio",    on_click=lambda _: self.cambiar(0), style=ft.ButtonStyle(color=self.c_violet_lt)),
                        ft.TextButton("servicios", on_click=lambda _: self.cambiar(1), style=ft.ButtonStyle(color=self.c_muted)),
                        ft.TextButton("resumen",   on_click=lambda _: self.cambiar(2), style=ft.ButtonStyle(color=self.c_muted)),
                        ft.TextButton("contacto",  on_click=lambda _: self.cambiar(3), style=ft.ButtonStyle(color=self.c_muted)),
                    ]),
                ],
            ),
        )

        # ── INICIO ──────────────────────────
        self.inicio = ft.Container(
            visible=True,
            padding=ft.padding.only(left=64, right=64, top=60, bottom=60),
            content=ft.Row(
                alignment="spaceBetween",
                vertical_alignment="center",
                controls=[
                    ft.Column(
                        expand=True,
                        spacing=18,
                        controls=[
                            self.badge("disponible · Colombia"),
                            self.status_text,
                            ft.Text("jeisonagutierrez@ucundinamarca.edu.co", size=14, color=self.c_violet_lt, font_family="monospace"),
                            self.titulo_nombre,
                            ft.Text(
                                "INGENIERO DE SOFTWARE & TECNICO EN SISTEMAS",
                                size=15, italic=True, color=self.c_muted,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "Estudiante de tercer semestre en la universidad de cundinamarca \n\n "
                                    "Tecnico en sistemas, con pasion por la programacion \n\n "
                                    "Especializado en mantenimiento preventivo y correctivo de hardware, soporte de instalacion de sistemas operativos",
                                    size=14, color=self.c_muted, width=480,
                                ),
                                border=ft.border.only(left=ft.border.BorderSide(2, "#4c2e8a")),
                                padding=ft.padding.only(left=18),
                            ),
                            ft.Row(
                                spacing=12,
                                controls=[
                                    ft.ElevatedButton(
                                        "ver servicios",
                                        on_click=lambda _: self.cambiar(1),
                                        bgcolor=self.c_violet,
                                        color=self.c_text,
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                    ),
                                    ft.OutlinedButton(
                                        "descargar CV",
                                        style=ft.ButtonStyle(
                                            color=self.c_muted,
                                            side=ft.BorderSide(0.5, "#2d3148"),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                ],
                            ),
                            ft.Row(
                                wrap=True, spacing=8,
                                controls=[
                                    self.skill_tag(s)
                                    for s in ["Python", "FastAPI", "flet", "Flask", "HTML5", "Git"]
                                ],
                            ),
                            ft.Container(
                                content=self.log_terminal,
                                padding=12,
                                bgcolor="#060608",
                                border_radius=8,
                                width=420,
                                border=ft.border.all(0.5, self.c_border),
                            ),
                        ],
                    ),

                    ft.Container(width=60),

                    ft.Column(
                        horizontal_alignment="center",
                        spacing=16,
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src="foto.png",
                                    width=310, height=310,
                                    fit="cover",
                                    border_radius=20,
                                ),
                                border=ft.border.all(1, "#4c2e8a"),
                                border_radius=20,
                                padding=4,
                                shadow=ft.BoxShadow(
                                    blur_radius=40,
                                    color="#3b1a7a",
                                    offset=ft.Offset(0, 8),
                                ),
                            ),
                            ft.Text(
                                "while(alive): code()",
                                color="#3d2a6e",
                                font_family="monospace",
                                italic=True,
                                size=13,
                            ),
                        ],
                    ),
                ],
            ),
        )

        # ── SERVICIOS ───────────────────────
        self.servicios = ft.Container(
            visible=False,
            padding=ft.padding.all(60),
            content=ft.Column(
                spacing=16,
                controls=[
                    self.section_header("// MÓDULO: SERVICIOS"),
                    self.card("Mantenimiento hardware", "Limpieza y mantenimiento preventivo y correctivo de hardware.", "hardware.png"),
                    self.card("Mantenimiento software", "Actualizaciones y soluciones de problemas de software.", "windows.png"),
                    self.card("Instalación de sistemas operativos", "instalacion de sistemas operativos windows y linux.", "Linux.png"),
                    self.card("Soporte técnico", "Asistencia técnica remota y presencial para resolver problemas.", "support.png"),
                ],
            ),
        )

        # ── RESUMEN ─────────────────────────
        self.resumen = ft.Container(
            visible=False,
            padding=ft.padding.all(60),
            content=ft.Column(
                spacing=20,
                controls=[
                    self.section_header("// MÓDULO: HISTORIAL_TÉCNICO"),
                    ft.Text("EXPERIENCIA_LABORAL", color=self.c_violet_lt, size=16, weight="bold", font_family="monospace"),
                    self.card(
                        "Técnico | Segura",
                        "Soporte remoto/presencial · Mantenimiento de computadores · instalación de redes · ",
                        "python.svg",
                    ),
                    ft.Container(height=4),
                    ft.Text("HABILIDADES_DEL_SISTEMA", color=self.c_violet_lt, size=16, weight="bold", font_family="monospace"),
                    ft.Container(
                        width=820,
                        padding=24,
                        bgcolor=self.c_surface,
                        border_radius=12,
                        border=ft.border.all(0.5, self.c_border),
                        content=ft.Column(
                            spacing=22,
                            controls=[
                                self.skill("Ofimática Experta", 0.87),
                                self.skill("Soporte & Hardware", 0.94),
                                self.skill("Diagnóstico y resolución de problemas técnicos", 0.89),
                                self.skill("Soporte al usuario", 0.97),
                            ],
                        ),
                    ),
                ],
            ),
        )

        # ── CONTACTO ────────────────────────
        self.contacto = ft.Container(
            visible=False,
            padding=ft.padding.all(60),
            expand=True,
            content=ft.Column(
                spacing=16,
                scroll="auto",
                controls=[
                    self.section_header("// ESTABLECIENDO_CONEXIÓN"),
                    self.card("Email", "guti092017@mail.com", "gmail.png", "mailto:guti092017@mail.com"),
                    self.card("GitHub", "github.com/JAG062003", "git.svg", "https://github.com/JAG062003"),
                    self.card("LinkedIn", "Perfil profesional", "linkedin.png", "https://www.linkedin.com/in/jeison-alexander-gutierrez-leal-a94a25204/"),
                ],
            ),
        )

        self.page.add(
            self.navbar,
            ft.Column(
                expand=True,
                scroll="auto",
                controls=[self.inicio, self.servicios, self.resumen, self.contacto],
            ),
        )

    # ─────────────────────────────────────────
    #  ANIMACIONES
    # ─────────────────────────────────────────

    async def animar_inicio(self):
        await self.escribir(self.status_text, "[ STATUS: ACTIVE ]  [ LOC: COLOMBIA ]  [ ROLE: ENG ]")
        await self.escribir(self.titulo_nombre, "Jeison Gutierrez")
        logs = [
            ("> [OK] Kernel loaded",         self.c_neon),
            ("> [OK] System initialized",    self.c_neon),
            ("> [OK] Security: Active",      self.c_neon),
            ("> [>>] Portfolio v2.0 running", self.c_violet_lt),
        ]
        for texto, color in logs:
            self.log_terminal.controls.append(
                ft.Text(texto, color=color, size=11, font_family="monospace")
            )
            self.page.update()
            await asyncio.sleep(0.3)

    async def escribir(self, control, texto):
        for i in range(len(texto) + 1):
            control.value = texto[:i] + "_"
            self.page.update()
            await asyncio.sleep(0.05)
        control.value = texto
        self.page.update()

    # ─────────────────────────────────────────
    #  NAVEGACIÓN
    # ─────────────────────────────────────────

    def cambiar(self, i):
        self.inicio.visible    = (i == 0)
        self.servicios.visible = (i == 1)
        self.resumen.visible   = (i == 2)
        self.contacto.visible  = (i == 3)
        self.page.update()


# ─────────────────────────────────────────────
async def main(page: ft.Page):
    app = PortafolioHacker(page)
    await app.animar_inicio()


ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir="assets")

import os
import flet as ft

async def main(page: ft.Page):
    app = PortafolioHacker(page)
    await app.animar_inicio()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))

    ft.run(
        target=main,
        port=port,
        view=ft.WEB_BROWSER,
        assets_dir="assets"
    )
