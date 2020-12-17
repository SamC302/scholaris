from rich.console import Console

from scholaris.Grades import Grade

console = Console()

grade_associate = {
            Grade.A: 'bold green',
            Grade.B: 'bold yellow',
            Grade.C: 'bold blue',
            Grade.D: 'bold red',
            Grade.E: 'bold white',
            Grade.NOGRADE: ''
        }