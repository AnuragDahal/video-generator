"use client"

import { GalleryVerticalEnd, MessageSquare, Plus, Trash2 } from "lucide-react"
import * as React from "react"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupAction,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail
} from "@/components/ui/sidebar"
import type { Conversation } from "@/lib/chat-store"

interface ChatSidebarProps extends React.ComponentProps<typeof Sidebar> {
  conversations: Conversation[];
  activeId: string | null;
  onConversationSelect: (id: string) => void;
  onCreate: () => void;
  onDelete: (id: string) => void;
}

export function ChatSidebar({
  conversations,
  activeId,
  onConversationSelect,
  onCreate,
  onDelete,
  ...props
}: ChatSidebarProps) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                <GalleryVerticalEnd className="size-4" />
              </div>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-semibold">NovaMind</span>
                <span className="truncate text-xs text-muted-foreground">Video AI Engine</span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <div className="flex items-center justify-between px-2 mb-2">
            <SidebarGroupLabel>Conversations</SidebarGroupLabel>
            <SidebarGroupAction onClick={onCreate} title="New Chat">
              <Plus className="size-4" />
            </SidebarGroupAction>
          </div>
          <SidebarMenu>
            {conversations.map((conv) => (
              <SidebarMenuItem key={conv.id}>
                <SidebarMenuButton
                  isActive={activeId === conv.id}
                  onClick={() => onConversationSelect(conv.id)}
                  tooltip={conv.title}
                >
                  <MessageSquare className="size-4 shrink-0" />
                  <span className="truncate">{conv.title}</span>
                </SidebarMenuButton>
                <SidebarMenuAction
                  className="peer-data-[active=true]:text-sidebar-accent-foreground"
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(conv.id);
                  }}
                >
                  <Trash2 className="size-4" />
                </SidebarMenuAction>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
         <div className="p-2">
            <p className="text-[10px] text-muted-foreground text-center uppercase tracking-widest font-medium opacity-50">
                NovaMind v1.0
            </p>
         </div>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
